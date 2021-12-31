import logging

from cliff.lister import Lister
import boto3.dynamodb
from src.services.environments_service import EnvironmentsService
from src.services.log_ingestion_streams_service import LogIngestionStreamsService


class EnvironmentsList(Lister):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = boto3.client('dynamodb')
        tables = client.list_tables()

        # Init services
        environments_svc = EnvironmentsService(self.app.config['dynamodb'])
        ingestion_streams_svc = LogIngestionStreamsService(self.app.config['dynamodb'])

        # Get list of items in tables
        environment_items = environments_svc.list()
        log_ingestion_stream_items = ingestion_streams_svc.list()

        # Checks to see if the number of environments is the same number of log ingestion streams and if not it raises
        # an error
        if len(environment_items[0].get('Items')) != len(log_ingestion_stream_items[0].get('Items')):
            raise ValueError("Number of environments does not match the number of log ingestion streams. Try "
                             "adding or removing an environment or log ingestion stream")

        rows = []
        # Creates each row that will be displayed in the table
        for i in range(len(environment_items)+1):
            row = {'environment': environment_items[0].get('Items')[i].get('name').get('S'),
                   'destination_arn': log_ingestion_stream_items[0].get('Items')[i].get('destination_arn').get('S'),
                   'iam_role_arn': log_ingestion_stream_items[0].get('Items')[i].get('iam_role_arn').get('S')
                   }
            rows.append(row)

        return ('Environment Name', 'Destination ARN', 'IAM Role ARN'), ((row.get('environment'),
                                                                          row.get('destination_arn'),
                                                                          row.get('iam_role_arn')) for row in rows)
