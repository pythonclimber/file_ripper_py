from os import path

import fileconstants as fc


def create_file_definitions(json_data):
    return [FileDefinition(file_def) for file_def in json_data[fc.FILE_DEFINITIONS]]


def validate_file_data(file_data):
    if fc.FILE_MASK not in file_data:
        raise ValueError(f'{fc.FILE_MASK} is a required property')

    if fc.FILE_TYPE not in file_data:
        raise ValueError(f'{fc.FILE_TYPE} is a required property')

    if file_data[fc.FILE_TYPE] == fc.DELIMITED and fc.DELIMITER not in file_data:
        raise ValueError(f'{fc.DELIMITER} is a required property for delimited files')

    if fc.FIELD_DEFINITIONS not in file_data or not file_data[fc.FIELD_DEFINITIONS]:
        raise ValueError(f'{fc.FIELD_DEFINITIONS} is a required property')

    if file_data[fc.FILE_TYPE] == fc.XML and fc.RECORD_ELEMENT_NAME not in file_data:
        raise ValueError(f'{fc.RECORD_ELEMENT_NAME} is a required property for xml files')

    if fc.EXPORT_DEFINITION not in file_data:
        raise ValueError(f'{fc.EXPORT_DEFINITION} is a required property')


class FieldDefinition:
    def __init__(self, file_data, file_type):
        if fc.FIELD_NAME not in file_data:
            raise ValueError('field_name is required for a valid FieldDefinition')

        if file_type == fc.FIXED and (fc.START_POSITION not in file_data or fc.FIELD_LENGTH not in file_data):
            raise ValueError('start_position and field_length are required for a fixed position file')

        self.field_name = file_data[fc.FIELD_NAME]
        self.start_position = file_data[fc.START_POSITION] if file_type == fc.FIXED else None
        self.field_length = file_data[fc.FIELD_LENGTH] if file_type == fc.FIXED else None
        self.xml_node_name = file_data[fc.XML_NODE_NAME] if fc.XML_NODE_NAME in file_data else None


class ExportDefinition:
    def __init__(self, file_data):
        if fc.EXPORT_TYPE not in file_data:
            raise ValueError(f'{fc.EXPORT_TYPE} is a required property')

        if file_data[fc.EXPORT_TYPE] == fc.API_EXPORT and fc.API_URL not in file_data:
            raise ValueError(f'{fc.API_URL} is a required property for an {fc.EXPORT_TYPE} of {fc.API_EXPORT}')

        if file_data[fc.EXPORT_TYPE] == fc.DATABASE_EXPORT and fc.DB_CONNECTION_STRING not in file_data:
            raise ValueError(f'{fc.DB_CONNECTION_STRING} is a required property for {fc.EXPORT_TYPE} '
                             f'of {fc.DATABASE_EXPORT}')

        if file_data[fc.EXPORT_TYPE] == fc.FILE_EXPORT and fc.OUTPUT_FILE_PATH not in file_data:
            raise ValueError(f'{fc.OUTPUT_FILE_PATH} is required for {fc.EXPORT_TYPE} of {fc.FILE_EXPORT}')

        self.export_type = file_data[fc.EXPORT_TYPE]
        self.api_url = file_data[fc.API_URL] if fc.API_URL in file_data else ''
        self.db_connection_string = file_data[fc.DB_CONNECTION_STRING] if fc.DB_CONNECTION_STRING in file_data else ''
        self.output_file_path = file_data[fc.OUTPUT_FILE_PATH] if fc.OUTPUT_FILE_PATH in file_data else ''
        self.http_headers = file_data[fc.HTTP_HEADERS] if fc.HTTP_HEADERS in file_data else {}
        self.collection_name = file_data[fc.COLLECTION_NAME] if fc.COLLECTION_NAME in file_data else ''
        self.database_name = file_data[fc.DATABASE_NAME] if fc.DATABASE_NAME in file_data else ''


class FileDefinition:
    def __init__(self, file_data):
        validate_file_data(file_data)

        self.file_mask = file_data[fc.FILE_MASK]
        self.file_type = file_data[fc.FILE_TYPE]
        self.export_definition = ExportDefinition(file_data[fc.EXPORT_DEFINITION])
        self.has_header = file_data[fc.HAS_HEADER] if fc.HAS_HEADER in file_data else False
        self.input_directory = file_data[fc.INPUT_DIRECTORY] if fc.INPUT_DIRECTORY in file_data else ''
        self.completed_directory = file_data[fc.COMPLETED_DIRECTORY] if fc.COMPLETED_DIRECTORY in file_data \
            else path.join(self.input_directory, 'completed')
        self.file_description = file_data[fc.FILE_DESCRIPTION] if fc.FILE_DESCRIPTION in file_data else ''

        self.delimiter = file_data[fc.DELIMITER] if fc.DELIMITER in file_data else ''
        self.record_element_name = file_data[fc.RECORD_ELEMENT_NAME] if file_data[fc.FILE_TYPE] == fc.XML else ''

        self.field_definitions = [FieldDefinition(obj, self.file_type) for obj in file_data[fc.FIELD_DEFINITIONS]]


class XmlFieldDefinition(FieldDefinition):
    def __init__(self, file_data):
        if fc.XML_NODE_NAME not in file_data:
            raise ValueError(f'{fc.XML_NODE_NAME} is a required field for xml file definition')

        super(XmlFieldDefinition, self).__init__(file_data, fc.XML)
        self.xml_node_name = file_data[fc.XML_NODE_NAME]
