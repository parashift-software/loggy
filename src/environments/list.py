import logging

from cliff.lister import Lister
import boto3.dynamodb


class EnvironmentsList(Lister):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        client = boto3.client('dynamodb')
        tables = client.list_tables()

        environment_items = []
        log_ingestion_stream_items = []
        for table in tables['TableNames']:
            # Look through the table names and get the environment and log ingestion streams items
            if "Environments" in table:
                environment_items.append(client.scan(TableName=table))
            if "LogIngestionStreams" in table:
                log_ingestion_stream_items.append(client.scan(TableName=table))

        # Checks to see if the number of environments is the same number of log ingestion streams and if not it raises
        # an error
        if len(environment_items[0].get('Items')) != len(log_ingestion_stream_items[0].get('Items')):
            raise ValueError("Number of environments does not match the number of log ingestion streams. Try "
                             "adding or removing an environment or log ingestion stream")


        rows = []
        # Creates each row that will be displayed in the table
        for i in range(len(environment_items)):
            row = {'environment': environment_items[0].get('Items')[i].get('name').get('S'),
                   'destination_arn': log_ingestion_stream_items[0].get('Items')[i].get('destination_arn').get('S'),
                   'iam_role_arn': log_ingestion_stream_items[0].get('Items')[i].get('iam_role_arn').get('S')
                   }
            rows.append(row)

        return ('Environment Name', 'Destination ARN', 'IAM Role ARN'), ((row.get('environment'),
                                                                          row.get('destination_arn'),
                                                                          row.get('iam_role_arn')) for row in rows)
