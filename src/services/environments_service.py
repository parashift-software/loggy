import boto3
import uuid


class EnvironmentsService:

    def __init__(self, dynamodb_config):
        self._dynamodb_config = dynamodb_config
        self._dynamodb = boto3.resource('dynamodb')
        self._dynamodb_client = boto3.client('dynamodb')

    def create(self, name):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['environments'])

        environment = {
            'id': str(uuid.uuid4()),
            'name': name
        }

        table.put_item(Item=environment)
        return environment

    def list(self):
        tables = self._dynamodb_client.list_tables()

        environments = []
        for table in tables['TableNames']:
            # Look through the table names and get the environment items
            if "Environments" in table:
                environments.append(self._dynamodb_client.scan(TableName=table))

        return environments
