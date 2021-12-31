import sys
import os
import json

from cliff.app import App
from cliff.commandmanager import CommandManager


class LoggyApp(App):

    def __init__(self):
        super(LoggyApp, self).__init__(
            description='AWS LogGroup-Kinesis Subscription Manager',
            version='0.1',
            command_manager=CommandManager('parashift.loggy'),
            deferred_help=True,
            )

        self.config = None

    def initialize_app(self, argv):
        config_path = '/etc/loggy/config.json'
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                self.config = json.loads(config_file.read())

    def prepare_to_run_command(self, cmd):
        pass

    def clean_up(self, cmd, result, err):
        pass


def main(argv=sys.argv[1:]):
    myapp = LoggyApp()
    return myapp.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
