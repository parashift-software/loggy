import boto3
import uuid


class LogIngestionStreamsService:

    def __init__(self, dynamodb_config):
        self._dynamodb_config = dynamodb_config
        self._dynamodb = boto3.resource('dynamodb')
        self._dynamodb_client = boto3.client('dynamodb')

    def create(self, destination_arn, iam_role_arn, environment_id):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['log_ingestion_streams'])

        stream = {
            'id': str(uuid.uuid4()),
            'environment_id': environment_id,
            'destination_arn': destination_arn,
            'iam_role_arn': iam_role_arn
        }

        table.put_item(Item=stream)
        return stream

    def list(self):
        tables = self._dynamodb_client.list_tables()

        log_ingestion_stream = []
        for table in tables['TableNames']:
            # Look through the table names and get the log ingestion streams items
            if "LogIngestionStreams" in table:
                log_ingestion_stream.append(self._dynamodb_client.scan(TableName=table))

        return log_ingestion_stream
