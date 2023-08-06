from pymongo import MongoClient
from elasticsearch import Elasticsearch
from progress.spinner import Spinner


class MongoElastic:
    def __init__(self, args):

        # mongo db connection
        self.mongo_host = args.get('mongo_host', 'localhost')
        self.mongo_port = args.get('mongo_port', None)
        self.mongo_max_pool_size = args.get('mongo_max_pool_size', 50)
        self.mongo_db_name = args.get('mongo_db_name', None)
        self.mongo_document_name = args.get('mongo_document_name', None)

        # elasticsearch connection
        self.es_host = args.get('es_host', ['localhost'])
        self.es_http_auth = args.get('es_http_auth', None)
        self.es_port = args.get('es_port', None)
        self.es_index_name = args.get('es_index_name', 'mongoelastic_index')
        self.es_doc_type = args.get('es_doc_type', 'mongoelastic_doc_type')
        self.use_ssl = args.get('use_ssl', False)
        self.ca_certs = args.get('ca_certs', None)

    def start(self, m_filter=None):
        m_filter = dict() if not m_filter else m_filter
        client = MongoClient(self.mongo_host, self.mongo_port, maxPoolSize=self.mongo_max_pool_size)
        db = client[self.mongo_db_name]
        document_name = db[self.mongo_document_name]

        mongo_where = m_filter.get('mongo_condition', {})
        # get all data from mongoDB db
        m_data = document_name.find(mongo_where)

        es = Elasticsearch(
            self.es_host,
            http_auth=self.es_http_auth if self.es_http_auth else None,
            port=self.es_port if self.es_port else None,
            use_ssl=self.use_ssl if self.use_ssl else False,
            ca_certs=self.ca_certs if self.ca_certs else None
        )
        i = 1
        spinner = Spinner('Importing... ')
        for line in m_data:
            docket_content = line
            # remove _id from mongo object
            del docket_content['_id']
            try:
                es.index(index=self.es_index_name, doc_type=self.es_doc_type,
                         id=i, body=docket_content)
            except Exception:
                pass
            i += 1
            spinner.next()
        client.close()
        return True
