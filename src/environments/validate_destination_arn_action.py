import argparse
import logging


class ValidateDestinationArnAction(argparse.Action):

    log = logging.getLogger(__name__)

    def __call__(self, parser, namespace, value, option_string=None):
        value_array = value.split(':')

        if len(value_array) < 6:
            raise ValueError('Please enter a correct length ARN for destination ARN')
        else:
            if not(value_array[0] == 'arn' and value_array[1] == 'aws' and
                   (value_array[2] == 'kinesis' or value_array[2] == 'firehose')):
                raise ValueError("Please enter a valid destination ARN")
        setattr(namespace, self.dest, value)
