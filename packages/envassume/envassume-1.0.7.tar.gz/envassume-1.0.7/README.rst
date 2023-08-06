envassume
=========

.. image:: https://img.shields.io/pypi/v/envassume.svg
    :target: https://pypi.python.org/pypi/envassume

.. image:: https://img.shields.io/pypi/pyversions/envassume.svg
    :target: https://pypi.python.org/pypi/envassume

.. image:: https://img.shields.io/pypi/l/envassume.svg
    :target: https://pypi.python.org/pypi/envassume

.. image:: https://travis-ci.org/wamonite/envassume.svg?branch=master
    :target: https://travis-ci.org/wamonite/envassume

.. image:: https://codecov.io/gh/wamonite/envassume/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/wamonite/envassume

Assume an AWS IAM role and execute a command with the assumed credentials. AWS API credentials to assume the role must be set as environment variables, and the command and arguments are executed in the same manner as envdir_.

.. _envdir: https://envdir.readthedocs.io/en/latest/

``envassume`` takes the effort out of assuming an AWS role from the command-line and copying/pasting the returned credentials to run a command. If you often need to do this:-

::

    $ aws sts assume-role --role-arn arn:aws:iam::123456789012:role/s3_access --role-session-name s3_access_session
    {
        "AssumedRoleUser": {
            "AssumedRoleId": "xxxxxxxxxxxxxxxxxxxxx:s3_access_session",
            "Arn": "arn:aws:sts::123456789012:assumed-role/s3_access/s3_access_session"
        },
        "Credentials": {
            "SecretAccessKey": "mmm",
            "SessionToken": "nnn",
            "Expiration": "2019-02-26T00:00:00Z",
            "AccessKeyId": "ooo"
        }
    }
    $ AWS_ACCESS_KEY_ID='ooo' AWS_SECRET_ACCESS_KEY='mmm' AWS_SESSION_TOKEN='nnn' aws s3 ls

It can be shortened to:-

::

    $ envassume arn:aws:iam::123456789012:role/s3_access aws s3 ls

Useful if you often need to test roles, or run scripts with assumed roles on AWS instances using credentials from the instance profile.

Install
-------

::

    pip install envassume

Usage
-----

::

    usage: envassume [-h] [-i EXTERNAL_ID] [ARN] command [argument [argument ...]]

    optional arguments:
        -h, --help              show this help message and exit
        -i, --id EXTERNAL_ID    external id
        ARN                     AWS role ARN to assume (required if not set by environment variable)

    environment variables:
        environment must contain valid AWS API credentials

        AWS_ASSUME_ROLE=ARN
            no options can be present before the command if this is defined

        AWS_ASSUME_ID=EXTERNAL_ID

License
-------

Copyright (c) 2017 Warren Moore

This software may be redistributed under the terms of the MIT License.
See the file LICENSE for details.

Contact
-------

::

          @wamonite     - twitter
           \_______.com - web
    warren____________/ - email
