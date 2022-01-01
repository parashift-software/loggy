import boto3


class CloudWatchLogGroupService:

    def __init__(self):
        self._client = boto3.client('logs')

    def list(self):
        log_groups = []

        paginator = self._client.get_paginator('describe_log_groups')
        iterator = paginator.paginate()
        for page in iterator:
            for log_group in page.get('logGroups', []):
                log_group['subscriptionFilters'] = self.get_subscription_filters(log_group.get('logGroupName'))
                log_groups.append(log_group)

        return log_groups

    def get_subscription_filters(self, log_group):
        subscription_filters = []

        paginator = self._client.get_paginator('describe_subscription_filters')
        iterator = paginator.paginate(logGroupName=log_group)
        for page in iterator:
            subscription_filters.extend(page.get('subscriptionFilters', []))

        return subscription_filters

    def subscribe_to_kinesis(self, log_group_name, destination_arn, iam_role_arn):
        self._client.put_subscription_filter(
            logGroupName=log_group_name,
            filterName='KINESIS',
            filterPattern='',
            destinationArn=destination_arn,
            roleArn=iam_role_arn,
            distribution='Random'
        )
