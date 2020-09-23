from typing import IO
from xml.etree.ElementTree import fromstring, parse

import fileconstants as fc


class FileService:
    def process(self, file: IO):
        return {fc.FILE_NAME: file.name, fc.RECORDS: self.process_file_records(file.readlines())}

    def process_file_records(self, lines):
        raise NotImplementedError('Please use a valid implementation of FileService to read files')

    @staticmethod
    def create_file_service(file_definition):
        if file_definition.file_type == fc.XML:
            return XmlFileService(file_definition)
        elif file_definition.file_type == fc.DELIMITED:
            return DelimitedFileService(file_definition)
        elif file_definition.file_type == fc.FIXED:
            return FixedFileService(file_definition)
        else:
            raise ValueError(f'file_definition is configured for unsupported file_type: {file_definition.file_type}')


class XmlFileService(FileService):
    def __init__(self, file_definition):
        self.file_definition = file_definition

    def process_file_records(self, lines):
        tree = fromstring(''.join(lines))

        records = []
        for item in tree.findall(f'./{self.file_definition.record_element_name}'):
            record = {}
            for field_def in self.file_definition.field_definitions:
                record[field_def.field_name] = item.find(f'{field_def.field_name}').text
            records.append(record)

        return records


class DelimitedFileService(FileService):
    def __init__(self, file_definition):
        self.file_definition = file_definition

    def process_file_records(self, lines):
        records = []
        if self.file_definition.has_header:
            lines.pop(0)

        for line in lines:
            records.append(self.process_line_fields(line))

        return records

    def process_line_fields(self, line):
        fields = [field.rstrip() for field in line.split(self.file_definition.delimiter)]
        record = {}

        field_count = len(self.file_definition.field_definitions)
        if field_count != len(fields):
            raise OSError('File records do not match file definition')

        for i in range(0, field_count):
            record[self.file_definition.field_definitions[i].field_name] = fields[i]
        return record


class FixedFileService(FileService):
    def __init__(self, file_definition):
        self.file_definition = file_definition

    def process_file_records(self, lines):
        records = []
        if self.file_definition.has_header:
            lines.pop(0)

        for line in lines:
            records.append(self.process_line_fields(line))

        return records

    def process_line_fields(self, line):
        record = {}
        for field_def in self.file_definition.field_definitions:
            end_position = field_def.start_position + field_def.field_length
            if end_position > len(line.rstrip()):
                raise IndexError(f'field {field_def.field_name} extends past the end of line')
            record[field_def.field_name] = line[field_def.start_position:end_position].rstrip()
        return record
