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
        log_group_svc = CloudWatchLogGroupService()

        # Load data
        self.log.info('Fetching log groups ...')
        log_groups = log_group_svc.list()

        self.log.info('Fetching environments ...')
        environments = EnvironmentsService(self.app.config['dynamodb']).list()

        self.log.info('Fetching log ingestion streams ...')
        ingestion_streams = LogIngestionStreamsService(self.app.config['dynamodb']).list()

        ingestion_streams_indexed = {}
        for ingestion_stream in ingestion_streams:
            ingestion_streams_indexed[ingestion_stream['environment_id']] = ingestion_stream

        # Subscription options
        options = self.generate_options(environments)

        for log_group in log_groups:
            if len(log_group.get('subscriptionFilters')) == 0:
                option = self.prompt_for_sub_environment(log_group, options)
                if not option:
                    # User asked to exit
                    return

                sub_environment_id = option['environment_id']
                if sub_environment_id:
                    ingestion_stream = ingestion_streams_indexed[sub_environment_id]
                    log_group_svc.subscribe_to_kinesis(
                        log_group['logGroupName'],
                        ingestion_stream['destination_arn'],
                        ingestion_stream['iam_role_arn']
                    )

    def prompt_for_sub_environment(self, log_group, options):
        self.log.info(f'\nWhich environment\'s log ingestion stream should the following log group be subscribed to?')
        self.log.info(f"{log_group['logGroupName']}\n")

        for idx, option in options.items():
            self.log.info(f'{idx}: {option["display"]}')
        self.log.info('q: Quit')

        selection = input('Selected option: ').strip().lower()
        if selection.isnumeric():
            selection = int(selection)

        if selection in ['q', 'quit', 'exit']:
            return None

        option = options.get(selection)
        if option:
            return option

        # User entered bad input. Try again
        return self.prompt_for_sub_environment(log_group, options)

    def generate_options(self, environments):
        counter = 1
        options = {}

        for environment in environments:
            options[counter] = {
                'display': environment['name'],
                'environment_id': environment['id']
            }
            counter += 1

        options['n'] = {
            'display': 'Never Subscribe',
            'environment_id': None
        }
        return options
