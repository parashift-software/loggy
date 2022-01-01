import boto3
import uuid


class LogIngestionStreamsService:

    def __init__(self, dynamodb_config):
        self._dynamodb_config = dynamodb_config
        self._dynamodb = boto3.resource('dynamodb')

    def list(self):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['log_ingestion_streams'])
        return table.scan().get('Items', [])

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
