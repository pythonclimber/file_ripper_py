import json

import requests

import fileconstants as fc
from filedefinition import ExportDefinition


def create_data_exporter(export_definition: ExportDefinition):
    if export_definition.export_type == fc.API_EXPORT:
        return ApiExporter(export_definition.api_url, export_definition.http_headers)
    if export_definition.export_type == fc.DATABASE_EXPORT:
        return DatabaseExporter(export_definition.db_connection_string)
    if export_definition.export_type == fc.FILE_EXPORT:
        return FileExporter(export_definition.output_file_path)
    return None


def send_data_to_api(data: dict, headers: dict, api_url: str) -> dict:
    response = requests.post(api_url, data=json.dumps(data), headers=headers)
    return json.loads(response.text)


class ApiExporter:
    def __init__(self, api_url, http_headers, api_sender=send_data_to_api):
        self.api_url = api_url
        self.api_sender = api_sender
        self.http_headers = http_headers

    def export_data(self, data):
        self.api_sender(data, self.http_headers, self.api_url)


class DatabaseExporter:
    def __init__(self, db_connection_string):
        self.db_connection_string = db_connection_string


class FileExporter:
    def __init__(self, output_file_path):
        self.output_file_path = output_file_path
