# -*- coding: utf-8 -*-
"""
envassume
"""

from __future__ import print_function
import sys
import os
from socket import gethostname
import re
import boto3
from botocore.exceptions import BotoCoreError
from .exceptions import EnvAssumeException, EnvAssumeHelpException
from .arguments import parse_arguments
from .usage import print_help, print_error


def apply_session_name_constraints(session_name):
    valid_session_name = re.sub(r'[^\w+=,.@\-]*', '', session_name)

    if not valid_session_name:
        raise EnvAssumeException('Empty session name')

    return valid_session_name[:64]


def assume_role(role_arn, external_id = None, session_name = None):
    if not external_id:
        external_id = os.environ.get('AWS_EXTERNAL_ID')

    if not session_name:
        session_name = 'envassume-' + gethostname()

    request = {
        'RoleArn': role_arn,
        'RoleSessionName': apply_session_name_constraints(session_name),
    }

    if external_id:
        request['ExternalId'] = external_id

    boto3_session = boto3.Session()
    sts_client = boto3_session.client('sts')
    try:
        response = sts_client.assume_role(**request)

    except BotoCoreError as ex:
        raise EnvAssumeException('{}'.format(ex))

    return response.get('Credentials') or {}


def update_env(credentials_lookup):
    credentials_list = (
        ('AccessKeyId', 'AWS_ACCESS_KEY_ID'),
        ('SecretAccessKey', 'AWS_SECRET_ACCESS_KEY'),
        ('SessionToken', 'AWS_SESSION_TOKEN'),
    )
    for credential_key, env_var_name in credentials_list:
        os.environ[env_var_name] = credentials_lookup[credential_key]


def exec_command(arg_list):
    try:
        os.execvpe(arg_list[0], arg_list, os.environ)

    except OSError as ex:
        raise EnvAssumeException('Unable to run command {}: {}'.format(arg_list[0], ex))

    raise EnvAssumeException('Unable to run command {}'.format(arg_list[0]))


def envassume():
    arg_lookup = parse_arguments(sys.argv)

    credentials_lookup = assume_role(arg_lookup.get('arn'), arg_lookup.get('external_id'))

    update_env(credentials_lookup)

    exec_command(arg_lookup['command'])


def run():
    try:
        envassume()

    except EnvAssumeHelpException:
        print_help()

    except EnvAssumeException as ex:
        print_error(ex)
        sys.exit(1)

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    run()
