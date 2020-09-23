import os
import unittest
from unittest.mock import Mock

import fileconstants as fc
from filedefinition import FileDefinition, create_file_definitions, FieldDefinition
from fileripper import FileRipper
from fileservice import XmlFileService, DelimitedFileService, FixedFileService, FileService


class FileDefinitionTests(unittest.TestCase):
    def setUp(self):
        self.json_data = {
            fc.FILE_DEFINITIONS: [
                {
                    fc.FILE_MASK: 'Valid-*.csv',
                    fc.FILE_TYPE: fc.DELIMITED,
                    fc.DELIMITER: ',',
                    fc.INPUT_DIRECTORY: os.getcwd(),
                    fc.FIELD_DEFINITIONS: [
                        {
                            fc.FIELD_NAME: 'name',
                            fc.START_POSITION: 0,
                            fc.FIELD_LENGTH: 12
                        }
                    ],
                    fc.EXPORT_DEFINITION: {
                        fc.EXPORT_TYPE: fc.API_EXPORT,
                        fc.API_URL: 'https://ohgnarly3-staging.herokuapp.com/person',
                        fc.DB_CONNECTION_STRING: 'mongodb://gnarly_user:Gnarly234@ds.mlab.com/gnarly_test',
                        fc.OUTPUT_FILE_PATH: '/users/asmitty/workspace/file.txt'
                    }
                }
            ]
        }

    def test_create_file_definitions(self):
        file_definitions = create_file_definitions(self.json_data)
        file_definition = file_definitions[0]
        self.assert_file_definition(file_definition)

    def test_create_file_definitions_xml_file(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE] = fc.XML
        self.json_data[fc.FILE_DEFINITIONS][0][fc.RECORD_ELEMENT_NAME] = 'record'
        self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS].append({fc.FIELD_NAME: 'address'})
        file_definitions = create_file_definitions(self.json_data)
        self.assert_file_definition(file_definitions[0])
        self.assertEqual('record', file_definitions[0].record_element_name)

    def test_create_file_definitions_fixed_file(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE] = fc.FIXED
        file_definitions = create_file_definitions(self.json_data)
        self.assert_file_definition(file_definitions[0])

    def test_create_file_definitions_invalid_json(self):
        self.json_data = {}
        self.assertRaises(KeyError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_missing_file_mask(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_MASK])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_missing_file_type(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_missing_field_definitions(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_delimited_file_missing_delimiter(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.DELIMITER])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_empty_field_definitions(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS][0])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_xml_file_missing_record_element_name(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE] = fc.XML
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_file_definition_missing_export(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_field_definition_missing_field_name(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS][0][fc.FIELD_NAME])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_field_definition_missing_start_position(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE] = fc.FIXED
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS][0][fc.START_POSITION])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_create_file_definitions_invalid_field_definition_missing_field_length(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE] = fc.FIXED
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS][0][fc.FIELD_LENGTH])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def assert_file_definition(self, file_definition):
        self.assertEqual(self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_MASK], file_definition.file_mask)
        self.assertEqual(self.json_data[fc.FILE_DEFINITIONS][0][fc.FILE_TYPE], file_definition.file_type)
        self.assertEqual(self.json_data[fc.FILE_DEFINITIONS][0][fc.DELIMITER], file_definition.delimiter)
        self.assertEqual(self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.EXPORT_TYPE],
                         file_definition.export_definition.export_type)
        self.assertEqual(self.json_data[fc.FILE_DEFINITIONS][0][fc.FIELD_DEFINITIONS][0][fc.FIELD_NAME],
                         file_definition.field_definitions[0].field_name)


class ExportDefinitionTests(FileDefinitionTests):
    def setUp(self):
        super(ExportDefinitionTests, self).setUp()

    def test_invalid_export_definition_missing_export_type(self):
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.EXPORT_TYPE])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_invalid_export_definition_api_export_missing_api_url(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.EXPORT_TYPE] = fc.API_EXPORT
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.API_URL])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_invalid_export_definition_database_export_missing_db_connection_string(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.EXPORT_TYPE] = fc.DATABASE_EXPORT
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.DB_CONNECTION_STRING])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)

    def test_invalid_export_definition_file_export_missing_output_file_path(self):
        self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.EXPORT_TYPE] = fc.FILE_EXPORT
        del (self.json_data[fc.FILE_DEFINITIONS][0][fc.EXPORT_DEFINITION][fc.OUTPUT_FILE_PATH])
        self.assertRaises(ValueError, create_file_definitions, self.json_data)


class FileConstantsTests(unittest.TestCase):
    def test_file_type(self):
        self.assertEqual(fc.FILE_TYPE, 'file_type')

    def test_file_mask(self):
        self.assertEqual(fc.FILE_MASK, 'file_mask')

    def test_delimited(self):
        self.assertEqual(fc.DELIMITED, 'DELIMITED')

    def test_fixed(self):
        self.assertEqual(fc.FIXED, 'FIXED')

    def test_xml(self):
        self.assertEqual(fc.XML, 'XML')

    def test_delimiter(self):
        self.assertEqual(fc.DELIMITER, 'delimiter')

    def test_created_at(self):
        self.assertEqual(fc.CREATED_AT, 'created_at')

    def test_created_by(self):
        self.assertEqual(fc.CREATED_BY, 'created_by')

    def test_has_header(self):
        self.assertEqual(fc.HAS_HEADER, 'has_header')

    def test_field_definitions(self):
        self.assertEqual(fc.FIELD_DEFINITIONS, 'field_definitions')

    def test_file_definitions(self):
        self.assertEqual(fc.FILE_DEFINITIONS, 'file_definitions')

    def test_field_name(self):
        self.assertEqual(fc.FIELD_NAME, 'field_name')

    def test_file_name(self):
        self.assertEqual(fc.FILE_NAME, 'file_name')

    def test_records(self):
        self.assertEqual(fc.RECORDS, 'records')

    def test_start_position(self):
        self.assertEqual(fc.START_POSITION, 'start_position')

    def test_field_length(self):
        self.assertEqual(fc.FIELD_LENGTH, 'field_length')

    def test_record_element_name(self):
        self.assertEqual(fc.RECORD_ELEMENT_NAME, 'record_element_name')

    def test_xml_node_name(self):
        self.assertEqual(fc.XML_NODE_NAME, 'xml_node_name')

    def test_input_directory(self):
        self.assertEqual(fc.INPUT_DIRECTORY, 'input_directory')

    def test_data_url(self):
        self.assertEqual(fc.API_URL, 'api_url')

    def test_completed_directory(self):
        self.assertEqual(fc.COMPLETED_DIRECTORY, 'completed_directory')

    def test_output_mode(self):
        self.assertEqual(fc.EXPORT_TYPE, 'export_type')

    def test_api_export(self):
        self.assertEqual(fc.API_EXPORT, 'API')

    def test_file_export(self):
        self.assertEqual(fc.FILE_EXPORT, 'FILE')

    def test_database_export(self):
        self.assertEqual(fc.DATABASE_EXPORT, 'DATABASE')

    def test_export_definition(self):
        self.assertEqual(fc.EXPORT_DEFINITION, 'export_definition')

    def test_file_description(self):
        self.assertEqual(fc.FILE_DESCRIPTION, 'file_description')

    def test_db_connection_string(self):
        self.assertEqual(fc.DB_CONNECTION_STRING, 'db_connection_string')

    def test_output_file_path(self):
        self.assertEqual(fc.OUTPUT_FILE_PATH, 'output_file_path')

    def test_http_headers(self):
        self.assertEqual(fc.HTTP_HEADERS, 'http_headers')

    def test_collection_name(self):
        self.assertEqual(fc.COLLECTION_NAME, 'collection_name')

    def test_database_name(self):
        self.assertEqual(fc.DATABASE_NAME, 'database_name')


class CreateFileServiceTests(unittest.TestCase):
    """Test cases for file service factory function code"""

    def setUp(self):
        self.file_data = {
            fc.FILE_MASK: "",
            fc.INPUT_DIRECTORY: '',
            fc.EXPORT_DEFINITION: {
                fc.EXPORT_TYPE: fc.API_EXPORT,
                fc.API_URL: 'http://www.google.com'
            },
            fc.FIELD_DEFINITIONS: [
                {
                    fc.FIELD_NAME: "Name"
                }
            ]
        }

    def test_create_file_service_xml_file_definition(self):
        """Create xml file service given and xml file definition"""
        file_definition = self.create_file_definition(fc.XML, 'record')
        file_service = FileService.create_file_service(file_definition)
        self.assertTrue(isinstance(file_service, XmlFileService))

    def test_create_file_service_delimited_file_definition(self):
        """Create delimited file service given a delimited file definition"""
        # arrange
        self.file_data[fc.DELIMITER] = "\t"
        file_definition = self.create_file_definition(fc.DELIMITED)
        # act
        file_service = FileService.create_file_service(file_definition)
        # assert
        self.assertTrue(isinstance(file_service, DelimitedFileService))

    def test_create_file_service_fixed_file_definition(self):
        """Create fixed file service given fixed file definition"""
        self.file_data[fc.FIELD_DEFINITIONS][0][fc.START_POSITION] = '0'
        self.file_data[fc.FIELD_DEFINITIONS][0][fc.FIELD_LENGTH] = '12'
        file_definition = self.create_file_definition(fc.FIXED)
        file_service = FileService.create_file_service(file_definition)
        self.assertTrue(isinstance(file_service, FixedFileService))

    def test_create_file_service_invalid_file_type(self):
        """Raise value error when invalid file type is created"""
        file_definition = self.create_file_definition('file_type')
        self.assertRaises(ValueError, FileService.create_file_service, file_definition)

    def create_file_definition(self, file_type, record_element_name=None):
        self.file_data[fc.FILE_TYPE] = file_type
        if record_element_name:
            self.file_data[fc.RECORD_ELEMENT_NAME] = record_element_name
        return FileDefinition(self.file_data)


class FileServiceTests(unittest.TestCase):
    def setUp(self):
        self.file_name = None
        self.file_data = {
            fc.FILE_MASK: "Valid-*.txt",
            fc.HAS_HEADER: True,
            fc.INPUT_DIRECTORY: '',
            fc.EXPORT_DEFINITION: {
                fc.EXPORT_TYPE: fc.API_EXPORT,
                fc.API_URL: 'http://www.google.com'
            },
            fc.FIELD_DEFINITIONS: [
                {
                    fc.FIELD_NAME: "name",
                    fc.START_POSITION: 0,
                    fc.FIELD_LENGTH: 13
                },
                {
                    fc.FIELD_NAME: "age",
                    fc.START_POSITION: 13,
                    fc.FIELD_LENGTH: 9
                },
                {
                    fc.FIELD_NAME: "dob",
                    fc.START_POSITION: 22,
                    fc.FIELD_LENGTH: 10
                }
            ]
        }

    def assert_valid_file_output(self, file_output, file_name):
        self.assertTrue(fc.FILE_NAME in file_output)
        self.assertEqual(file_name, file_output[fc.FILE_NAME])
        self.assertTrue(fc.RECORDS in file_output)
        self.assertTrue(isinstance(file_output[fc.RECORDS], list))
        self.assertEqual(4, len(file_output[fc.RECORDS]))
        self.assert_valid_records(file_output)

    def assert_valid_records(self, file_output):
        self.assertEqual('Aaron', file_output[fc.RECORDS][0]['name'])
        self.assertEqual('39', file_output[fc.RECORDS][0]['age'])
        self.assertEqual('09/04/1980', file_output[fc.RECORDS][0]['dob'])
        self.assertEqual('Gene', file_output[fc.RECORDS][1]['name'])
        self.assertEqual('61', file_output[fc.RECORDS][1]['age'])
        self.assertEqual('01/15/1958', file_output[fc.RECORDS][1]['dob'])
        self.assertEqual('Xander', file_output[fc.RECORDS][2]['name'])
        self.assertEqual('4', file_output[fc.RECORDS][2]['age'])
        self.assertEqual('11/22/2014', file_output[fc.RECORDS][2]['dob'])

    def test_process_records_not_implemented(self):
        file_service = FileService()
        self.assertRaises(NotImplementedError, file_service.process_file_records, [])

    def tearDown(self):
        try:
            if self.file_name:
                os.remove(self.file_name)
        except Exception as ex:
            print(ex)


class DelimitedFileServiceTests(FileServiceTests):
    def setUp(self):
        super(DelimitedFileServiceTests, self).setUp()
        self.file_data[fc.FILE_TYPE] = fc.DELIMITED
        self.file_data[fc.DELIMITER] = "|"
        self.file_definition = FileDefinition(self.file_data)
        self.file_service = DelimitedFileService(self.file_definition)
        self.file_name = 'Valid-delimited-09032019.txt'
        with open(self.file_name, 'w') as f:
            f.write('Name|Age|DOB\n')
            f.write('Aaron|39|09/04/1980\n')
            f.write('Gene|61|01/15/1958\n')
            f.write('Xander|4|11/22/2014\n')
            f.write('Mason|12|04/13/2007\n')

    def test_process_given_comma_delimiter(self):
        with open(self.file_name, 'r') as file:
            file_output = self.file_service.process(file)
            self.assert_valid_file_output(file_output, self.file_name)

    def test_process_given_invalid_file(self):
        with open(self.file_name, 'r') as file:
            self.file_definition.field_definitions.remove(self.file_definition.field_definitions[-1])
            self.assertRaises(OSError, self.file_service.process, file)


class FixedFileServiceTests(FileServiceTests):
    def setUp(self):
        super(FixedFileServiceTests, self).setUp()
        self.file_data[fc.FILE_TYPE] = fc.FIXED
        self.file_definition = FileDefinition(self.file_data)
        self.file_service = FileService.create_file_service(self.file_definition)
        self.file_name = 'Valid-fixed-09032019.txt'
        with open(self.file_name, 'w') as f:
            f.write('Name         Age      DOB       \n')
            f.write('Aaron        39       09/04/1980\n')
            f.write('Gene         61       01/15/1958\n')
            f.write('Xander       4        11/22/2014\n')
            f.write('Mason        12       04/13/2007\n')

    def test_process(self):
        with open(self.file_name, 'r') as file:
            file_output = self.file_service.process(file)
            self.assert_valid_file_output(file_output, self.file_name)

    def test_process_invalid_file_records_too_short(self):
        with open(self.file_name, 'r') as file:
            self.file_definition.field_definitions.append(
                FieldDefinition({fc.FIELD_NAME: 'address', fc.START_POSITION: 32, fc.FIELD_LENGTH: 2}, fc.FIXED))
            self.assertRaises(IndexError, self.file_service.process, file)


class XmlFileServiceTests(FileServiceTests):
    def setUp(self):
        super(XmlFileServiceTests, self).setUp()
        self.file_data[fc.FILE_TYPE] = fc.XML
        self.file_data[fc.RECORD_ELEMENT_NAME] = 'person'
        self.file_definition = FileDefinition(self.file_data)
        self.file_service = XmlFileService(self.file_definition)
        self.file_name = 'Valid-xml-09032019.txt'
        with open(self.file_name, 'w') as f:
            self.file = f
            f.write('<people>\n')
            self.write_xml_record('Aaron', 39, '09/04/1980')
            self.write_xml_record('Gene', 61, '01/15/1958')
            self.write_xml_record('Xander', 4, '11/22/2014')
            self.write_xml_record('Mason', 12, '04/13/2007')
            f.write('</people>\n')

    def write_xml_record(self, name, age, dob):
        self.file.write('\t<person>\n')
        self.file.write(f'\t\t<name>{name}</name>\n')
        self.file.write(f'\t\t<age>{age}</age>\n')
        self.file.write(f'\t\t<dob>{dob}</dob>\n')
        self.file.write('\t</person>\n')

    def test_process(self):
        with open(self.file_name, 'r') as file:
            file_output = self.file_service.process(file)
            self.assert_valid_file_output(file_output, self.file_name)

    def test_process_given_invalid_file_missing_attribute(self):
        with open(self.file_name, 'r') as file:
            self.file_definition.field_definitions.append(FieldDefinition({fc.FIELD_NAME: 'address'}, fc.XML))
            self.assertRaises(AttributeError, self.file_service.process, file)


class DatabaseExporterTests(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_export_data(self):
        pass


class FileRipper2Tests(FileServiceTests):
    def setUp(self) -> None:
        super(FileRipper2Tests, self).setUp()

        self.file_service = FileService()
        file_service_factory = Mock(return_value=self.file_service)

        self.expected = {}
        self.file_service.process = Mock(return_value=self.expected)

        self.file_data[fc.FILE_TYPE] = fc.FIXED
        self.file_ripper = FileRipper(file_service_factory)
        self.file_definition = FileDefinition(self.file_data)

    def test_rip_file_returns_file_output(self):
        file_names = self.create_files()
        with open(file_names[0], 'r') as file:
            actual = self.file_ripper.rip_file(file, self.file_definition)
        self.assertIs(self.expected, actual)
        self.delete_files()

    def test_rip_file_not_a_file(self):
        self.file_service.process = Mock(side_effect=AttributeError)
        self.assertRaises(AttributeError, self.file_ripper.rip_file, {}, self.file_definition)

    def test_rip_files_returns_file_output_list(self):
        file_count = 2
        file_names = self.create_files(file_count)
        for file_name in file_names:
            with open(file_name, 'r') as file:
                files = [file for _ in range(0, 2)]
                actual = self.file_ripper.rip_files(files, self.file_definition)
                self.assertEqual(len(files), len(actual))
                [self.assertIs(self.expected, a) for a in actual]
        self.delete_files(file_count)

    def test_rip_files_not_files(self):
        self.file_service.process = Mock(side_effect=AttributeError)
        self.assertRaises(AttributeError, self.file_ripper.rip_files, [{}, {}], self.file_definition)

    @staticmethod
    def create_files(total_files=1):
        file_names = []
        for i in range(0, total_files):
            with open(f'Valid-{i}.txt', 'w') as file:
                file_names.append(file.name)
                file.write(f'hello from {i}')
        return file_names

    @staticmethod
    def delete_files(total_files=1):
        for i in range(0, total_files):
            os.remove(f'Valid-{i}.txt')


if __name__ == '__main__':
    unittest.main()
