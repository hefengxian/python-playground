import pymysql
import yaml
from elasticsearch import Elasticsearch
from threading import Thread, Lock, current_thread
import datetime
import time
import math
import logging
import coloredlogs
import multiprocessing
import os

logger = logging.getLogger('SyncData2ES')
coloredlogs.install(level='INFO', logger=logger,
                    fmt='[%(asctime)s] %(processName)s.%(threadName)s.%(levelname)s %(message)s')
date_fmt = '%Y-%m-%d %H:%M:%S'
cur_dir = os.path.dirname(__file__)
mappings = {
    "mappings": {
        "properties": {
            "article_content_fingerprint": {
                "type": "keyword"
            },
            "article_detail_id": {
                "type": "long"
            },
            "article_extracted_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "article_pubtime": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "article_record_md5_id": {
                "type": "keyword"
            },
            "article_title_fingerprint": {
                "type": "keyword"
            },
            "client_id": {
                "type": "long"
            },
            "created_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "domain_code": {
                "type": "keyword"
            },
            "domain_score": {
                "type": "integer"
            },
            "emotion_type": {
                "type": "byte"
            },
            "junk_score": {
                "type": "integer"
            },
            "media_type_code": {
                "type": "keyword"
            },
            "relative_score": {
                "type": "integer"
            },
            "sentiment_score": {
                "type": "integer"
            },
            "similar_record_oldest_id": {
                "type": "long"
            },
            "source_type": {
                "type": "keyword"
            },
            "subject_id": {
                "type": "long"
            },
            "total_score": {
                "type": "integer"
            },
            "user_confirm_emotion_type": {
                "type": "byte"
            },
            "user_id": {
                "type": "long"
            },
            "user_last_process_time": {
                "type": "date",
                "format": "yyyy-MM-dd HH:mm:ss"
            },
            "user_process_status": {
                "type": "keyword"
            },
            "website_no": {
                "type": "keyword"
            }
        }
    }
}


def get_es():
    return Elasticsearch(['192.168.1.217', '192.168.1.218'])


def get_conn():
    # 读取数据库配置
    config = yaml.load(open(cur_dir + '/config.yml', 'r'), Loader=yaml.FullLoader)
    # 连接数据库
    db = pymysql.connect(**config['DB'], cursorclass=pymysql.cursors.DictCursor)
    return db


def get_fields():
    """获取查询的字段"""
    # mapping = json.load(open(os.getcwd() + '/../config/kwm-list-mapping.json', 'r'))
    # return mapping['mapping']['properties'].keys()
    return [
        'sas.article_content_fingerprint',
        'sas.article_detail_id',
        'sas.article_extracted_time',
        'sas.article_pubtime',
        'sas.article_record_md5_id',
        'sas.article_title_fingerprint',
        'sas.client_id',
        'sas.created_time',
        'sas.domain_code',
        'sas.domain_score',
        'sas.emotion_type',
        'sas.junk_score',
        'sas.media_type_code',
        'sas.relative_score',
        'sas.sentiment_score',
        'sas.similar_record_oldest_id',
        'sas.source_type',
        'sas.subject_id',
        'sas.total_score',
        'ao.user_confirm_emotion_type',
        'ao.user_id',
        'ao.user_last_process_time',
        'ao.user_process_status',
        'sas.website_no',
    ]


def list_chunk(lst, n):
    """
    将一个 List 分成 N 份
    :param lst: 要拆分的 list
    :param n: 拆分的份数
    :return: 生成器
    """
    list_len = len(lst)
    chunk_size = math.ceil(list_len / n)
    for i in range(0, list_len, chunk_size):
        yield lst[i:i + chunk_size]


def get_last_sync_time():
    filename = cur_dir + '/last_sync_time.txt'
    now = datetime.datetime.now()

    end = now.strftime(date_fmt)
    try:
        r = open(filename, mode='r')
        start = r.readline()
        datetime.datetime.strptime(start, date_fmt)
    except:
        start = now.strftime('%Y-%m-%d 00:00:00')
    finally:
        w = open(filename, 'w')
        w.write(end)
        w.flush()

    return {
        'start': start,
        'end': end
    }


def main():
    _task_start_time = time.time()
    # 时间分段间隔
    part_offset = 3600 * 1
    # 启动的线程数量
    thread_count = 5
    # CPU 核数
    cpu_count = math.ceil(multiprocessing.cpu_count() / 2)
    tasks = list()

    date_range = get_last_sync_time()
    start = date_range['start']
    end = date_range['end']

    # todo 现在没有容错机制，如果失败了，进度还是往前走的
    start_date = datetime.datetime.strptime(start, date_fmt)
    end_date = datetime.datetime.strptime(end, date_fmt)

    logger.info('开始同步，本次同步时间区间：【%s, %s】，任务拆分间隔 %ss, 启动 %s 个进程，%s 个线程' % (start, end, part_offset, cpu_count, thread_count))

    second_offset = (end_date - start_date).total_seconds()
    times = 1
    if second_offset > part_offset:
        times = math.ceil(second_offset / part_offset)

    _start = start_date
    _end = start_date
    for i in range(0, times):
        _start = _end
        _end += datetime.timedelta(seconds=part_offset)
        if _end >= end_date:
            _end = end_date

        task = {
            "start": _start.strftime(date_fmt),
            "end": (_end - datetime.timedelta(seconds=1)).strftime(date_fmt),
        }

        for tbl_idx in range(0, 100):
            tasks.append({"tbl_index": f'{tbl_idx}', **task})

    logger.info('本次同步拆分为 %s 个任务' % len(tasks))

    def sync_process(task_chunk):

        def sync_thread():
            while True:
                # 获取任务
                if len(task_chunk) == 0:
                    break

                _task = task_chunk.pop()
                logger.info('还剩 %s 个任务，当前任务%s' % (len(task_chunk), _task))
                tbl_name = 'stat_article_subject_' + _task['tbl_index']
                start_time = _task['start']
                end_time = _task['end']

                sql = f"""
                    /* Sync data 2 ES */
                    SELECT 
                        {','.join(get_fields())}
                    FROM 
                        {tbl_name} sas
                        LEFT JOIN article_operation ao ON sas.article_detail_id = ao.article_detail_id
                    WHERE
                        sas.created_time BETWEEN %s AND %s
                    """

                # 获取数据库链接
                db = get_conn()
                # 获取查询数据
                with db.cursor() as cursor:
                    _db_start = time.time()
                    cursor.execute(sql, [start_time, end_time])
                    rst = cursor.fetchall()
                    logger.debug("从数据库获 %s 表取得 %s 条记录，耗时 %.2fs" % (tbl_name, len(rst), time.time() - _db_start))

                # 处理数据
                _ps_start = time.time()
                indices = set()
                index_data = []
                for r in rst:
                    # 获取索引名称
                    idx_name = f"kwm-list-{r['article_extracted_time'].strftime('%Y-%m-%d')}"
                    indices.add(idx_name)

                    # 合成 ID
                    _id = f"{r['client_id']}-{r['subject_id']}-{r['article_detail_id']}"
                    # 组成 Action & Meta 信息
                    index_data.append({'index': {"_index": idx_name, "_id": _id}})

                    # 日期转字符串
                    for date_field in ('article_extracted_time', 'article_pubtime',
                                       'created_time', 'user_last_process_time'):
                        if isinstance(r[date_field], datetime.datetime):
                            r[date_field] = r[date_field].strftime('%Y-%m-%d %H:%M:%S')

                    index_data.append(r)
                logger.debug("处理数据库取出数据 %s 条记录，耗时 %.2fs" % (len(rst), time.time() - _ps_start))

                # 获取 ES 客户端
                # ES client 是线程安全的，可以为多个线程设置一个全局的实例
                # 但不是进程安全的，多个进程要设置多个实例
                _es_start = time.time()
                es = get_es()

                # 检查索引，不存在就创建
                for idx_name in indices:
                    exists = es.indices.exists(idx_name)
                    if not exists:
                        # 创建
                        es.indices.create(idx_name, mappings, ignore=400)

                # print(json.dumps(index_data, indent=True))
                if len(index_data) > 0:
                    resp = es.bulk(body=index_data, request_timeout=300)
                logger.debug("提交 ES 索引 %s 条记录，耗时 %.2fs" % (len(rst), time.time() - _es_start))

        # 启动线程
        threads = []
        for j in range(0, thread_count):
            # t = SyncTask(task_chunk=task_chunk, name=f'Thread-{j}')
            t = Thread(target=sync_thread, name=f'Thread-{j}')
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

    # 开启进程处理
    processes = []
    for t_chunk in list(list_chunk(tasks, cpu_count)):
        p = multiprocessing.Process(target=sync_process, args=(t_chunk, ))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
    logger.info("本次同步一共耗时 %.2fs" % (time.time() - _task_start_time))


if __name__ == '__main__':
    main()
    # get_fields()
