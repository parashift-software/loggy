import json
import logging

from cliff.command import Command
from src.services.log_groups_service import CloudWatchLogGroupService
from src.services.environments_service import EnvironmentsService
from src.services.log_ingestion_streams_service import LogIngestionStreamsService
from src.services.log_groups_blacklist_service import LogGroupsBlacklistService


class Audit(Command):

    def __init__(self, app, app_args):
        super().__init__(app, app_args)

    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        log_group_svc = CloudWatchLogGroupService()
        log_group_blacklist_svc = LogGroupsBlacklistService(self.app.config['dynamodb'])

        # Load data
        self.log.info('Fetching environments ...')
        environments = EnvironmentsService(self.app.config['dynamodb']).list()

        self.log.info('Fetching log ingestion streams ...')
        ingestion_streams = LogIngestionStreamsService(self.app.config['dynamodb']).list()
        ingestion_streams_indexed = {}
        for ingestion_stream in ingestion_streams:
            ingestion_streams_indexed[ingestion_stream['environment_id']] = ingestion_stream

        self.log.info('Fetching blacklisted log groups ...')
        blacklisted_log_group_arns = log_group_blacklist_svc.list()

        self.log.info('Fetching log groups ...')
        log_groups = log_group_svc.list()
        log_groups = self.non_blacklisted_log_groups(log_groups, blacklisted_log_group_arns)

        self.log.info('Fetching log group subscriptions ...')
        log_group_subscriptions = {}
        for log_group in log_groups:
            log_group_name = log_group['logGroupName']
            subscription = log_group_svc.get_subscription_filters(log_group_name)
            log_group_subscriptions[log_group_name] = subscription
        log_groups = self.non_subscribed_log_groups(log_groups, log_group_subscriptions)

        self.log.info('Fetching log group tags ...')
        log_group_tags = {}
        for log_group in log_groups:
            log_group_name = log_group['logGroupName']
            tags = log_group_svc.get_tags(log_group_name)
            log_group_tags[log_group_name] = tags

        # Subscription options
        options = self.generate_options(environments)

        # Do audit
        for log_group in log_groups:
            log_group_name = log_group['logGroupName']
            log_group['tags'] = log_group_tags[log_group_name]
            option = self.prompt_for_sub_environment(log_group, options)
            if not option:
                # User asked to exit
                return

            sub_environment_id = option['environment_id']
            if sub_environment_id:
                ingestion_stream = ingestion_streams_indexed[sub_environment_id]
                log_group_svc.subscribe_to_kinesis(
                    log_group_name,
                    ingestion_stream['destination_arn'],
                    ingestion_stream['iam_role_arn']
                )
            else:
                log_group_blacklist_svc.create(log_group['arn'])

    def prompt_for_sub_environment(self, log_group, options):
        self.log.info(f'\nWhich environment\'s log ingestion stream should the following log group be subscribed to?')
        self.log.info(f"Name: {log_group['logGroupName']}")

        tags = log_group['tags']
        if tags:
            self.log.info('Tags:')
            for key, value in tags.items():
                self.log.info(f'{key}: {value}')
            self.log.info('')
        else:
            self.log.info('Tags: None\n')

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

    def non_blacklisted_log_groups(self, log_groups, blacklisted_arns):
        non_blacklisted_log_groups = []

        for log_group in log_groups:
            if log_group['arn'] not in blacklisted_arns:
                non_blacklisted_log_groups.append(log_group)

        return non_blacklisted_log_groups

    def non_subscribed_log_groups(self, log_groups, subscriptions):
        non_subbed_log_groups = []

        for log_group in log_groups:
            subs = subscriptions[log_group['logGroupName']]
            if len(subs) == 0:
                non_subbed_log_groups.append(log_group)

        return non_subbed_log_groups
