import operator
import os
from functools import reduce
from typing import List

import yaml
from awscli.clidriver import create_clidriver

from ofxcloudsync import load_sync_ofx


def aws_cli(*cmd):
    """runs the cmd in the awscli

    "inspired" by https://github.com/boto/boto3/issues/358#issuecomment-372086466
    """
    old_env = dict(os.environ)
    try:

        # Environment
        env = os.environ.copy()
        env['LC_CTYPE'] = u'en_US.UTF'
        os.environ.update(env)
        # Run awscli in the same process
        exit_code = create_clidriver().main(cmd)

        # Deal with problems
        if exit_code > 0:
            raise RuntimeError('AWS CLI exited with code {}'.format(exit_code))
    finally:
        os.environ.clear()
        os.environ.update(old_env)


def s3sync(bucket: str, root: str, folders: List[str]) -> None:
    """calls the aws command to sync the bucket to root only including folders

    :param bucket: bucket to be synced
    :param root: path of local folder to sync to
    :param folders: list of folders to sync
    :return: None
    """
    folder_search = reduce(operator.iconcat, [('--include', f'"{f}/*"') for f in folders], [])
    aws_cli(
        's3', 'sync',
        f's3://{bucket}',
        root,
        '--exclude', '"*"',
        *folder_search)


def run_local_sync() -> None:
    """load a config file and call s3sync

    :param config_file_path: path of config file
    :return: None
    """
    config = load_sync_ofx()

    s3sync(
        config['bucket'],
        config['root_folder'],
        config['sync']
    )

