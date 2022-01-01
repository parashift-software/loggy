import logging

from cliff.lister import Lister

class BlacklistLogGroupClear(Lister):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        return ""