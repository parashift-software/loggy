import json
import logging

from cliff.command import Command
from src.services.log_groups_service import CloudWatchLogGroupService
from src.services.environments_service import EnvironmentsService
from src.services.log_ingestion_streams_service import LogIngestionStreamsService


class Audit(Command):

    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        # Load data
        log_groups = CloudWatchLogGroupService().list()
        environments = EnvironmentsService(self.app.config['dynamodb']).list()
        ingestion_streams = LogIngestionStreamsService(self.app.config['dynamodb']).list()

        # Subscription options
        options = self.generate_options(environments)

        for log_group in log_groups:
            if len(log_group.get('subscriptionFilters')) == 0:
                option = self.prompt_for_sub_environment(log_group, options)

    def prompt_for_sub_environment(self, log_group, options):
        self.log.info(f'Which environment\'s log ingestion stream should the following log group be subscribed to?')
        self.log.info(f"{log_group['logGroupName']}\n")

        for idx, option in options.items():
            self.log.info(f'{idx}: {option["display"]}')

        selection = input('Selected option #: ')
        selection = int(selection.strip())

        return options[selection]

    def generate_options(self, environments):
        counter = 1
        options = {}

        for environment in environments:
            options[counter] = {
                'display': environment['name'],
                'environment_id': environment['id']
            }
            counter += 1

        options[counter] = {
            'display': 'Never Subscribe',
            'environment_id': None
        }
        return options
