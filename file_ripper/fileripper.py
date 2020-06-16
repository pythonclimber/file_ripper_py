from typing import IO

from filedefinition import FileDefinition
from fileservice import create_file_service


class FileRipper:
    def __init__(self, file_service_factory=None):
        self.file_service_factory = file_service_factory if file_service_factory is not None else create_file_service

    def rip_file(self, file: IO, file_definition: FileDefinition):
        # file_service = create_file_service(file_definition)
        pass

    def rip_files(self, files: list[IO], file_definition: FileDefinition):
        pass

    def find_and_rip_files(self, files_path: str, file_definition: FileDefinition):
        pass