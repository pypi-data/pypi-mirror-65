"""
Build Script local logging and configuration variables

    - Python3 only
    - Requirement to set artifact which contains PACKAGE name
    - log_mode sets type of logging (i.e. 'STREAM' or 'FILE')

"""
import os
import sys
import subprocess


artifact = 'DESCRIPTION.rst'
enable_logging = True
log_filename = ''
log_path = ''
log_mode = 'STREAM'


def _region_list():
    """Returns a static list of AWS regions for bash completion"""
    return [
        'eu-north-1',
        'ap-south-1',
        'eu-west-3',
        'eu-west-2',
        'eu-west-1',
        'ap-northeast-2',
        'ap-northeast-1',
        'sa-east-1',
        'ca-central-1',
        'ap-southeast-1',
        'ap-southeast-2',
        'eu-central-1',
        'us-east-1',
        'us-east-2',
        'us-west-1',
        'us-west-2'
    ]


script_config = {
    "PROJECT": {
        "PACKAGE": 'rulemanager',
    },
    "LOGGING": {
        "ENABLE_LOGGING": enable_logging,
        "LOG_FILENAME": log_filename,
        "LOG_PATH": log_path,
        "LOG_MODE": log_mode,
        "SYSLOG_FILE": False
    }
}
