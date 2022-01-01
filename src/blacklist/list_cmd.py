import logging

from cliff.lister import Lister
from src.services.log_groups_blacklist_service import LogGroupsBlacklistService


class BlacklistLogGroupList(Lister):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        blacklisted_log_groups = LogGroupsBlacklistService(
            self.app.config['dynamodb']
        ).list()

        display_rows = []
        for log_stream in blacklisted_log_groups:
            display_rows.append((log_stream,))

        return ('Blacklisted Log Groups',), display_rows
