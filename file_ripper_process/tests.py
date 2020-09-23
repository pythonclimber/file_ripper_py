import json
import os
import unittest
from unittest.mock import MagicMock

import file_ripper.fileconstants as fc
from file_ripper.filedefinition import FileDefinition
from file_ripper_process.process import process_file_definition, execute_process


class FileRipperProcessTests(unittest.TestCase):
    def setUp(self):
        self.json_data = self.create_file_def_json()
        self.file_name = 'Valid-09092019.csv'
        self.definitions_file = 'file_definitions.json'
        with open(self.file_name, 'w') as file:
            file.write("Name,Age,DOB\n")
            file.write("Jason,99,01/01/1970")
        with open(self.definitions_file, 'w') as file:
            file.write(json.dumps(self.create_file_defs_json(self.json_data)))

    def test_process_file_definition_given_delimited_file(self):
        file_definition = FileDefinition(self.json_data)
        data_sender = MagicMock()
        file_mover = MagicMock()
        process_file_definition(file_definition, data_sender, file_mover)
        data_sender.assert_called_once()
        file_mover.assert_called_once()

    def test_execute_process(self):
        file_processor = MagicMock()
        execute_process(self.definitions_file, file_processor)
        file_processor.assert_called_once()

    def tearDown(self):
        try:
            if self.file_name:
                os.remove(self.file_name)
            if self.definitions_file:
                os.remove(self.definitions_file)
        except Exception as ex:
            print(ex)

    @staticmethod
    def create_file_def_json():
        return {
            fc.FILE_MASK: 'Valid-*.csv',
            fc.FILE_TYPE: fc.DELIMITED,
            fc.DELIMITER: ',',
            fc.HAS_HEADER: True,
            fc.INPUT_DIRECTORY: os.getcwd(),
            fc.FIELD_DEFINITIONS: [
                {fc.FIELD_NAME: 'name'},
                {fc.FIELD_NAME: 'age'},
                {fc.FIELD_NAME: 'dob'}
            ],
            fc.EXPORT_DEFINITION: {
                fc.EXPORT_TYPE: fc.API_EXPORT,
                fc.API_URL: 'http://www.google.com'
            }
        }

    @staticmethod
    def create_file_defs_json(file_def):
        return {
            fc.FILE_DEFINITIONS: [
                file_def
            ]
        }