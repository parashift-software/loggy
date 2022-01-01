import logging

from cliff.lister import Lister
from src.services.environments_service import EnvironmentsService
from src.services.log_ingestion_streams_service import LogIngestionStreamsService


class EnvironmentsList(Lister):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        environments = EnvironmentsService(
            self.app.config['dynamodb']
        ).list()

        environment_names = {}
        while len(environments) > 0:
            environment = environments.pop()
            environment_names[environment['id']] = environment['name']

        ingestion_streams = LogIngestionStreamsService(
            self.app.config['dynamodb']
        ).list()

        display_rows = []
        for ingestion_stream in ingestion_streams:
            display_rows.append((
                environment_names[ingestion_stream['environment_id']],
                ingestion_stream['destination_arn'],
                ingestion_stream['iam_role_arn']
            ))

        return (
                   'Environment Name',
                   'Destination ARN',
                   'IAM Role ARN'
               ), display_rows
