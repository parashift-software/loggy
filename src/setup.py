import logging

from cliff.command import Command


class Setup(Command):
    """A simple command that prints a message."""

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.log.info('Hello World!!!')
