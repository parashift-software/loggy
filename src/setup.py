import logging
import json

from cliff.command import Command


class Setup(Command):
    """A simple command that prints a message."""

    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('Hello World!!!')
        self.log.info(f'Config: {json.dumps(self.app.config)}')
