#!/usr/bin/python3
# -*- coding: utf-8 -*-

import traceback
from atexit import register as atexit_register
from json import dumps
from os import makedirs, path
from shutil import rmtree
from sys import exit, stderr
from logging import error, info, warning

try:
    from loguru import logger
    catch = logger.catch
except ImportError:
    def catch(x):
        print('Setup in progress?')

try:
    from .cli import Cli
    from .cli.args import get_cli_arguments
    from .fs import get_temp_path, get_info
    from .info import Info
    from .meta import __version__
except ImportError:
    error('Setup in progress?')

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'


@atexit_register
def before_shutdown():
    temp_dir = get_temp_path()
    path.isdir(temp_dir) and rmtree(temp_dir)


def _init_cli(args, _info):
    error_lvl = -5
    try:
        _info.start()
        cli_mode = Cli(args, _info)
        cli_mode.start()
        code = 0
    except Exception as e:
        traceback.print_tb(e.__traceback__, error_lvl, file=stderr)
        code = 1
        _info.set_error(e)
    return code


def _run_util(args) -> tuple:
    parse_args = args.parse_args()
    _info = Info(parse_args)
    code = _init_cli(args, _info)

    if parse_args.print_json:
        _info = dumps(
            _info.get(),
            indent=2,
            separators=(',', ': '),
            sort_keys=True,
        )
    else:
        _info = []

    return code, _info


def _update_all(args):
    parse_args = args.parse_args()
    info('Update all')
    multi_info = {}

    dst = parse_args.destination
    json_info = get_info(dst)

    for i in json_info:
        parse_args.manga_name = i['manga_name']
        parse_args.url = i['url']
        code, _info = _run_util(args)
        multi_info[i['directory']] = _info
    parse_args.quiet or (parse_args.print_json and print(multi_info))


@catch
def main():
    if ~__version__.find('alpha'):
        warning('Alpha release! There may be errors!')
    print('\n'.join((
        'Please remember that all sites earn on advertising.',
        'Remember to visit them from your browser.',
        'Thanks!\n'
    )), file=stderr)

    temp_path = get_temp_path()
    path.isdir(temp_path) or makedirs(temp_path)

    args = get_cli_arguments()
    parse_args = args.parse_args()

    try:
        code, _info = _run_util(args)
        parse_args.quiet or (parse_args.print_json and print(_info))
    except KeyboardInterrupt:
        error('\nUser interrupt')
        code = 1

    exit(code)


if __name__ == '__main__':
    main()
