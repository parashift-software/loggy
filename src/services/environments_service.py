import boto3
import uuid
import logging


class EnvironmentsService:

    def __init__(self, dynamodb_config):
        self._dynamodb_config = dynamodb_config
        self._dynamodb = boto3.resource('dynamodb')

    log = logging.getLogger(__name__)

    def list(self):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['environments'])
        return table.scan().get('Items', [])

    def create(self, name):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['environments'])

        environment = {
            'id': str(uuid.uuid4()),
            'name': name
        }

        table.put_item(Item=environment)
        return environment

    def delete(self, environment_id):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['environments'])

        table.delete_item(
            Key={
                'id': environment_id
            }
        )
        self.log.info(f'Successfully deleted {environment_id} environment')
