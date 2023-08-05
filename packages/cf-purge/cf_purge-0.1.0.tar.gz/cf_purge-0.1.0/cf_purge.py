#!/usr/bin/env python
"""
Invalidate easily your CloudFront distribution.
"""
VERSION = (0, 1, 0)
__version__ = '.'.join([str(i) for i in VERSION])
__author__ = 'Anthony Monthe (ZuluPro)'
__url__ = 'https://github.com/ZuluPro/cf-purge'
__email__ = 'anthony.monthe@gmail.com'

import argparse
from datetime import datetime
import logging
import sys
import time
import boto3
import botocore

logger = logging.getLogger('cf_purge')


def get_default_reference():
    return datetime.now().strftime('%y%m%d%H%M%S%f')


def main():
    parser = argparse.ArgumentParser(
        description="Invalidate AWS CloudFront's cache."
    )
    parser.add_argument('-a', '--access-key', required=False)
    parser.add_argument('-s', '--secret-key', required=False)
    parser.add_argument('-d', '--distribution', required=True)
    parser.add_argument(
        '-c', '--caller-reference', required=False,
        default=get_default_reference(),
        help="Unique identifier for invalidation request, default is "
             "a timestamp."
    )
    parser.add_argument('paths', nargs='+')

    parser.add_argument('-t', '--track', required=False, action='store_true',
                        help="Wait until the end of purge.")
    parser.add_argument('-v', '--verbose', action='count', default=0)

    parsed_args = parser.parse_known_args()[0]

    logger.setLevel(30-parsed_args.verbose*10)
    logger.addHandler(logging.StreamHandler())

    cloudfront = boto3.client(
        'cloudfront',
        aws_access_key_id=parsed_args.access_key,
        aws_secret_access_key=parsed_args.secret_key
    )
    response = cloudfront.create_invalidation(
        DistributionId=parsed_args.distribution,
        InvalidationBatch={
            'CallerReference': parsed_args.caller_reference,
            'Paths': {
                'Quantity': len(parsed_args.paths),
                'Items': parsed_args.paths
            }
        }
    )
    logger.debug(response)

    if parsed_args.track:
        invalidation = response['Invalidation']
        invalidation_id = invalidation['Id']
        while 1:
            if invalidation['Status'] == 'InProgress':
                logger.info('Purge done')
                break
            logger.info('Purge in progess')
            time.sleep(5)
            invalidation = cloudfront.get_invalidation(
                DistributionId=parsed_args.distribution,
                Id=invalidation_id,
            )['Invalidation']
            logger.debug(invalidation)


if __name__ == '__main__':
    try:
        main()
    except botocore.exceptions.ClientError as err:
        sys.stderr.write(err.args[0])
        sys.exit(1)
