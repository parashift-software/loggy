import logging
import boto3


class LogGroupsBlacklistService:

    def __init__(self, dynamodb_config):
        self._dynamodb_config = dynamodb_config
        self._dynamodb = boto3.resource('dynamodb')

    log = logging.getLogger(__name__)

    def list(self):
        blacklisted_log_groups = []

        table = self._dynamodb.Table(self._dynamodb_config['tables']['log_group_blacklist'])

        for item in table.scan().get('Items', []):
            blacklisted_log_groups.append(item['arn'])

        return blacklisted_log_groups

    def create(self, arn):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['log_group_blacklist'])

        blacklist = {
            'arn': arn
        }

        table.put_item(Item=blacklist)
        return blacklist

    def delete(self, arn):
        table = self._dynamodb.Table(self._dynamodb_config['tables']['log_group_blacklist'])

        table.delete_item(
            Key={
                'arn': arn
            }
        )
        self.log.info(f'Successfully deleted {arn} from blacklist')

    def clear(self):
        for arn in self.list():
            self.delete(arn)
