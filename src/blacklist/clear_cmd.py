import logging

from cliff.command import Command

from src.services.log_groups_blacklist_service import LogGroupsBlacklistService


class BlacklistLogGroupClear(Command):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        LogGroupsBlacklistService(self.app.config['dynamodb']).clear()
