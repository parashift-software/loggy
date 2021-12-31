import json
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
        parser.add_argument('environment_name')
        parser.add_argument('destination_arn')
        parser.add_argument('iam_role_arn')
        return parser

    def take_action(self, parsed_args):
        # Load required inputs
        environment_name = parsed_args.environment_name
        destination_arn = parsed_args.destination_arn
        iam_role_arn = parsed_args.iam_role_arn

        # Init services
        environments_svc = EnvironmentsService(self.app.config['dynamodb'])
        ingestion_streams_svc = LogIngestionStreamsService(self.app.config['dynamodb'])

        # Create environment and ingestion stream
        environment = environments_svc.create(parsed_args.name)
        self.log.info(f'Created environment: {json.dumps(environment)}')

        stream = ingestion_streams_svc.create(destination_arn, iam_role_arn, environment['id'])
        self.log.info(f'Created log ingestion stream: {json.dumps(stream)}')
