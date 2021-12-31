import logging
import json

from cliff.command import Command


class EnvironmentsAdd(Command):
    """A simple command that prints a message."""

    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('we addin stuff bruh')
        # self.log.info(json.dumps(parsed_args))
