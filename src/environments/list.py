import logging

from cliff.command import Command


class EnvironmentsList(Command):
    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('TODO: List environments')
