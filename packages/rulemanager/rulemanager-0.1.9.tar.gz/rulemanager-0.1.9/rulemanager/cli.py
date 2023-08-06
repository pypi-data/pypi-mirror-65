"""

Amazon CloudWatch Rule Converter, GPL v3 License

Copyright (c) 2020-2021 Blake Huber

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the 'Software'), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""
import os
import sys
import re
import datetime
import json
import inspect
import argparse
import boto3
import threading
from botocore.exceptions import ClientError
from libtools import stdout_message, logd
from libtools.js import export_iterobject
from libtools.oscodes_unix import exit_codes
from rulemanager.table import setup_table
from rulemanager.config import script_config
from rulemanager.about import about_object
from rulemanager.help import help_menu
from rulemanager import __version__, PACKAGE, logger

# globals
module = os.path.basename(__file__)


def account_number(profile):
    """Retrieves AWS Account Number"""
    session = boto3.Session(profile_name=profile)
    client = session.client('sts')
    return client.get_caller_identity()['Account']


def get_target_rules(profile, rgn, keyword='all'):
    """
    Returns CloudWatch Rules if exist based on search keyword
    """
    session = boto3.Session(profile_name=profile)
    client = session.client('events', region_name=rgn)
    r = client.list_rules()['Rules']
    if keyword == 'all':
        return [x for x in r]
    return [x for x in r if re.search(str(keyword), x['Name'], re.IGNORECASE)]


def _debug_output(*args):
    """additional verbose information output"""
    for arg in args:
        if os.path.isfile(arg):
            print('Filename {}'.format(arg.strip(), 'lower'))
        elif str(arg):
            print('String {} = {}'.format(getattr(arg.strip(), 'title'), arg))


def default_region():
    """Returns default AWS Region, if set"""
    return os.getenv('AWS_DEFAULT_REGION') or 'us-east-1'


def _get_regions():
    client = boto3.client('ec2')
    return [x['RegionName'] for x in client.describe_regions()['Regions']]


def format_pricefile(key):
    """Adds path delimiter and color formatting to output artifacts"""
    region = key.split('/')[0]
    pricefile = key.split('/')[1]
    delimiter = '/'
    return region + delimiter + pricefile


def package_version():
    """
    Prints package version and requisite PACKAGE info
    """
    print(about_object)
    sys.exit(exit_codes['EX_OK']['Code'])


def source_environment(env_variable):
    """
    Sources all environment variables
    """
    return {
        'duration_days': read_env_variable('DEFAULT_DURATION'),
        'page_size': read_env_variable('PAGE_SIZE', 700),
        'bucket': read_env_variable('S3_BUCKET', None)
    }.get(env_variable, None)


def options(parser, help_menu=False):
    """
    Summary:
        parse cli parameter options

    Returns:
        TYPE: argparse object, parser argument set

    """
    parser.add_argument("-D", "--debug", dest='debug', action='store_true', default=False, required=False)
    parser.add_argument("-d", "--disable", dest='disable', action='store_true', default=False, required=False)
    parser.add_argument("-e", "--enable", dest='enable', action='store_true', default=False, required=False)
    parser.add_argument("-h", "--help", dest='help', action='store_true', default=False, required=False)
    parser.add_argument("-k", "--keyword", dest='keyword', default=None, nargs='?', type=str, required=False)
    parser.add_argument("-p", "--profile", dest='profile', default='default', nargs='?', type=str, required=False)
    parser.add_argument("-r", "--region", dest='region', default=default_region(), nargs='?', type=str, required=False)
    parser.add_argument("-v", "--view", dest='view', action='store_true', default=False, required=False)
    parser.add_argument("-V", "--version", dest='version', action='store_true', default=False, required=False)
    return parser.parse_known_args()


def enable_rule(profile, rgn, keyword):
    """Enable (activate) specified CloudWatch rules"""
    session = boto3.Session(profile_name=profile)
    client = session.client('events', region_name=rgn)

    # extract cw rule names
    names = [x['Name'] for x in get_target_rules(profile, rgn, keyword)]

    if len(names) == 0:
        stdout_message('No CloudWatch rules found to enable', prefix='WARN')
        return False

    for name in names:
        try:
            r = client.enable_rule(Name=name)
            httpstatus = r['ResponseMetadata']['HTTPStatusCode']
            if str(httpstatus).startswith('20'):
                stdout_message('CloudWatch rule {} set to enabled.'.format(name))
            else:
                stdout_message('Failed to set CloudWatch rule {} to enabled.'.format(name), prefix='WARN')
        except ClientError as e:
            logger.exception('Boto ClientError: {}'.format(e))
            continue
    return True


def disable_rule(profile, rgn, keyword):
    """Enable (activate) specified CloudWatch rules"""
    session = boto3.Session(profile_name=profile)
    client = session.client('events', region_name=rgn)

    # extract cw rule names
    names = [x['Name'] for x in get_target_rules(profile, rgn, keyword)]

    if len(names) == 0:
        stdout_message('No CloudWatch rules found to enable', prefix='WARN')
        return False

    for name in names:
        try:
            r = client.disable_rule(Name=name)
            httpstatus = r['ResponseMetadata']['HTTPStatusCode']
            if str(httpstatus).startswith('20'):
                stdout_message('CloudWatch rule {} disabled.'.format(name))
            else:
                stdout_message('Failed to disable CloudWatch rule {}.'.format(name), prefix='WARN')
        except ClientError as e:
            logger.exception('Boto ClientError: {}'.format(e))
            continue
    return True


def init():
    """
    Initialize spot price operations; process command line parameters
    """

    parser = argparse.ArgumentParser(add_help=False)

    try:

        args, unknown = options(parser)

    except Exception as e:
        stdout_message(str(e), 'ERROR')
        return False

    if args.debug:
        stdout_message('PACKAGE: {}'.format(PACKAGE), prefix='DBUG')
        stdout_message('module: {}'.format(module), prefix='DBUG')
        stdout_message('module_path: {}'.format(os.path.join(PACKAGE, module)), prefix='DBUG')
        # log status
        logger.info('Environment variable status:')
        logger.info('\t- REGION: {}'.format(args.region))
        logger.info('\t- DBUGMODE is: {}'.format(args.debug))

    if args.help or (len(sys.argv) == 1):
        help_menu()
        return False

    elif args.version:
        package_version()
        return True

    elif args.view and args.keyword:
        account = account_number(args.profile)
        return setup_table(
                    get_target_rules(args.profile, args.region, args.keyword),
                    account,
                    args.region
                )

    elif args.view:
        account = account_number(args.profile)
        return setup_table(get_target_rules(args.profile, args.region), account, args.region)

    elif (args.enable and args.keyword) and not args.disable:
        account = account_number(args.profile)
        setup_table(
                    get_target_rules(args.profile, args.region, args.keyword),
                    account,
                    args.region
                )
        if enable_rule(args.profile, args.region, args.keyword):
            setup_table(
                        get_target_rules(args.profile, args.region, args.keyword),
                        account,
                        args.region
                    )

    elif (args.disable and args.keyword) and not args.enable:
        account = account_number(args.profile)
        setup_table(
                    get_target_rules(args.profile, args.region, args.keyword),
                    account,
                    args.region
                )
        if disable_rule(args.profile, args.region, args.keyword):
            setup_table(
                        get_target_rules(args.profile, args.region, args.keyword),
                        account,
                        args.region
                    )
