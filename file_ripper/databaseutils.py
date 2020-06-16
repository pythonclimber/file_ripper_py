import pymongo

from filedefinition import ExportDefinition


def create_db_sender(export_definition: ExportDefinition):
    return MongoDbSender(export_definition)


class MongoDbSender:
    def __init__(self, export_definition: ExportDefinition):
        self.connection_string = export_definition.db_connection_string
        self.database_name = export_definition.database_name
        self.collection_name = export_definition.collection_name

    def send_data(self, data):
        client = pymongo.MongoClient(self.connection_string, tlsAllowInvalidCertificates=True)
        db = client[self.database_name]
        return db[self.collection_name].insert_many(data)
