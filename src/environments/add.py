import logging

from cliff.command import Command
from src.services.environments_service import EnvironmentsService
from src.services.log_ingestion_streams_service import LogIngestionStreamsService


class EnvironmentsAdd(Command):
    """A simple command that prints a message."""

    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(EnvironmentsAdd, self).get_parser(prog_name)
        parser.add_argument('name')
        return parser

    def take_action(self, parsed_args):
        environment_name = parsed_args.name
        environments_svc = EnvironmentsService(self.app.config['dynamodb'])

        self.log.info(f'Creating environment \'{environment_name}\'')
        environments_svc.create(parsed_args.name)
