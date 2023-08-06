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
from elasticsearch import Elasticsearch


es_connection_object = Elasticsearch(['localhost'],use_ssl=False)

config = {
    'mongo_host': 'YOUR_MONGO_HOST',
    'mongo_port': YOUR_MONGO_PORT,
    'mongo_db_name': 'YOUR_MONGO_DB_NAME',
    'mongo_document_name': 'YOUR_MONGO_DOCUMENT_NAME',
    'es_connection': es_connection_object
    'es_index_name':'TEST_INDEX'
    'es_doc_type':'test_doc_type'
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