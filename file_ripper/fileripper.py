from typing import IO, List

from filedefinition import FileDefinition
from fileservice import FileService


class FileRipper:
    def __init__(self, file_service_factory=None, file_repository=None):
        self.file_service_factory = file_service_factory if file_service_factory is not None \
            else FileService.create_file_service

    def rip_file(self, file: IO, file_definition: FileDefinition):
        file_service = self.file_service_factory(file_definition)
        return file_service.process(file)

    def rip_files(self, files: List[IO], file_definition: FileDefinition):
        return [self.rip_file(f, file_definition) for f in files]
