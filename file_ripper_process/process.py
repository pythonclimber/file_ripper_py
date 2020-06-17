import json
import os
from datetime import datetime
from glob import glob

from file_ripper_data.dataexport import create_data_exporter
from file_ripper.filedefinition import create_file_definitions, FileDefinition
from file_ripper.filelogger import create_file_ripper_logger
from file_ripper.fileservice import create_file_service


logger = create_file_ripper_logger()


def move_file_to_completed(file_def: FileDefinition, file_name: str) -> None:
    source = os.path.join(file_def.input_directory, file_name)
    destination = os.path.join(file_def.completed_directory, file_name)
    if not os.path.exists(file_def.completed_directory):
        os.mkdir(file_def.completed_directory)
    os.rename(source, destination)


def process_file_definition(file_definition, data_exporter_factory=create_data_exporter, file_mover=move_file_to_completed):
    file_service = create_file_service(file_definition)
    os.chdir(file_definition.input_directory)
    data_sender = data_exporter_factory(file_definition.export_definition)
    for file_name in glob(file_definition.file_mask):
        logger.info(f'Processing file {file_name}...')
        with open(file_name, 'r') as file:
            data_sender.export_data(file_service.process(file))
            file_mover(file_definition, file_name)


def execute_process(definitions_file, file_def_processor=process_file_definition):
    logger.info(f"Starting file-ripper at {datetime.now().isoformat(' ', timespec='milliseconds')}")
    with open(definitions_file, 'r') as file:
        file_definitions = create_file_definitions(json.loads(file.read()))
        for file_def in file_definitions:
            file_def_processor(file_def)
