import boto3
import uuid


class EnvironmentsService:

    def __init__(self, dynamodb_config):
        self._dynamodb_config = dynamodb_config
        self._dynamodb = boto3.resource('dynamodb')

    def create(self, name):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['environments'])

        environment = {
            'id': str(uuid.uuid4()),
            'name': name
        }

        table.put_item(Item=environment)
        return environment
