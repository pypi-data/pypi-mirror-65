# mongoDB to elasticsearch

[![PyPI](https://img.shields.io/pypi/v/mongoelastic?color=green)](https://pypi.org/project/mongoelastic/)


***mongoelastic*** stands for MongoDB to Elasticsearch. Through this you can import data from mongoDB to elasticsearch.

---

## Installation

### Install mongoelastic from PyPI: <br />
`pip install mongoelastic` <br />

## Usage




* Here is the sample code 
```shell
from mongoelastic.mongoelastic import MongoElastic

config = {
    'mongo_host': 'YOUR_MONGO_HOST',
    'mongo_port': YOUR_MONGO_PORT,
    'mongo_db_name': 'YOUR_MONGO_DB_NAME',
    'mongo_document_name': 'YOUR_MONGO_DOCUMENT_NAME',
    'es_host': ['YOUR_ES_HOST'], # in list
    'es_http_auth': ('ES_USER', 'ES_PASSWORD'), # in tuple
    'es_port': ES_PORT,
    'es_index_name': 'ES_INDEX_NAME',
    'es_doc_type': 'ES_DOC_TYPE_NAME',
    'use_ssl':True/False,
    'ca_certs':'PATH'  
}
obb = MongoElastic(config)
obb.start()


# You can also filter query MongoDB like:
m_filter = {'mongo_condition':{"_id" : "5d9740bc245fb21097e82c11"}}
obb.start(m_filter)  
```


## License

[![Licence](https://img.shields.io/badge/Licence-MIT-GREEN.svg)](https://pypi.org/project/mongoelastic/)

***If you like the project, support by star***