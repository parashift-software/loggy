import logging

from cliff.command import Command

from src.services.environments_service import EnvironmentsService
from src.services.log_ingestion_streams_service import LogIngestionStreamsService


class EnvironmentsDelete(Command):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(EnvironmentsDelete, self).get_parser(prog_name)
        parser.add_argument('environment_name')
        return parser

    def take_action(self, parsed_args):
        # Load required inputs
        environment_name = parsed_args.environment_name

        # Init services
        environments_svc = EnvironmentsService(self.app.config['dynamodb'])
        ingestion_streams_svc = LogIngestionStreamsService(self.app.config['dynamodb'])

        environment_id = None
        for environment in environments_svc.list():
            if environment['name'] == environment_name:
                environment_id = environment['id']
                break
        if not environment_id:
            self.log.info(f'Did not find the {environment_name} environment')
            return

        log_ingestion_stream_id = None
        for log_ingestion_stream in ingestion_streams_svc.list():
            if log_ingestion_stream['environment_id'] == environment_id:
                log_ingestion_stream_id = log_ingestion_stream['id']
                break

        ingestion_streams_svc.delete(log_ingestion_stream_id)
        environments_svc.delete(environment_id)
