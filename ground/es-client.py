from datetime import datetime
from elasticsearch import Elasticsearch

es = Elasticsearch(['192.168.1.217', '192.168.1.218'])

resp = es.indices.exists('kwm-list-sample')

print(resp)
