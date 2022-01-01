import json
import logging
import boto3

from cliff.command import Command
from src.services.log_groups_service import CloudWatchLogGroupService


class LogGroupList(Command):

    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        log_groups = CloudWatchLogGroupService().list()
        self.log.info(f'Log Groups: {json.dumps(log_groups)}')
