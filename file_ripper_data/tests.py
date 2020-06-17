import unittest
from unittest.mock import Mock

from file_ripper_data.databaseutils import create_db_sender, MongoDbSender
from file_ripper.filedefinition import ExportDefinition
import file_ripper.fileconstants as fc
from file_ripper_data.dataexport import create_data_exporter, ApiExporter, DatabaseExporter, FileExporter


class CreateDbSenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.export_definition = ExportDefinition({fc.EXPORT_TYPE: fc.DATABASE_EXPORT,
                                                   fc.DB_CONNECTION_STRING: 'connection_string',
                                                   fc.DATABASE_NAME: 'database_name',
                                                   fc.COLLECTION_NAME: 'collection_name'})

    def test_send_data(self) -> None:
        sender = create_db_sender(self.export_definition)
        self.assertTrue(isinstance(sender, MongoDbSender))
        self.assertEqual(sender.collection_name, 'collection_name')
        self.assertEqual(sender.database_name, 'database_name')
        self.assertEqual(sender.connection_string, 'connection_string')


class MongoDbSenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.export_definition = ExportDefinition({
            fc.EXPORT_TYPE: fc.DATABASE_EXPORT,
            fc.COLLECTION_NAME: 'People',
            fc.DATABASE_NAME: 'gnarly_test',
            fc.DB_CONNECTION_STRING: 'mongodb+srv://dbuser:OhGnarly123@cluster0-hds1u.mongodb.net/test?retryWrites=true&w=majority'
        })

    def test_send_data(self):
        mongo_sender = MongoDbSender(self.export_definition)
        result = mongo_sender.send_data([{'name': 'Jim', 'age': 45, 'dob': '08/15/1974'}])
        self.assertIsNotNone(result)


class CreateDataExporterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.export_data = {}

    def test_create_data_exporter_given_api_export_type(self):
        self.export_data[fc.EXPORT_TYPE] = fc.API_EXPORT
        self.export_data[fc.API_URL] = 'api url'
        export_definition = ExportDefinition(self.export_data)
        data_exporter = create_data_exporter(export_definition)
        self.assertTrue(isinstance(data_exporter, ApiExporter))

    def test_create_data_exporter_given_database_export_type(self):
        self.export_data[fc.EXPORT_TYPE] = fc.DATABASE_EXPORT
        self.export_data[fc.DB_CONNECTION_STRING] = 'connection string'
        export_definition = ExportDefinition(self.export_data)
        data_exporter = create_data_exporter(export_definition)
        self.assertTrue(isinstance(data_exporter, DatabaseExporter))

    def test_create_data_exporter_given_file_export_type(self):
        self.export_data[fc.EXPORT_TYPE] = fc.FILE_EXPORT
        self.export_data[fc.OUTPUT_FILE_PATH] = 'output file path'
        export_definition = ExportDefinition(self.export_data)
        data_exporter = create_data_exporter(export_definition)
        self.assertTrue(isinstance(data_exporter, FileExporter))


class ApiExporterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api_url = 'api url'
        self.api_sender = Mock()
        self.headers = {}
        self.api_exporter = ApiExporter(self.api_url, self.headers, self.api_sender)

    def test_export_data(self):
        data = {}
        self.api_exporter.export_data(data)
        self.api_sender.assert_called_with(data, self.headers, self.api_url)