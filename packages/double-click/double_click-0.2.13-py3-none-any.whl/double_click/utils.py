import json
import os
import subprocess
import sys
from pathlib import Path

try:
    from distutils import sysconfig_get_python_lib as get_python_lib
except ImportError:
    # There doesn't seem to be any consistency on this import so have to handle both import types.
    from distutils.sysconfig import get_python_lib

from mdv.markdownviewer import main as mdv
from requests import Response

CLI_THEME = float(os.getenv('CLI_THEME', 1057.4342))


def echo(output):
    """Formats and displays the provided output

    :param output: Supports int, str, dict, list(dict()), list, & Response
    :return:
    """
    if isinstance(output, dict) or isinstance(output, list):
        try:
            print(json.dumps(output, indent=2))
        except (TypeError, ValueError):
            print(str(output))
    elif isinstance(output, Response):
        if output.status_code is None:
            err = f"#Server Error \n" \
                f"> {output.url} - {output.text}"
            print(mdv(md=err, theme=CLI_THEME, c_theme=CLI_THEME))
        elif output.status_code in [200, 201]:
            try:
                print(json.dumps(output.json(), indent=4))
            except json.decoder.JSONDecodeError:
                print(output.text)
        elif output.status_code in [401, 403]:
            print(mdv(md="#You do not have permissions to view this resource", theme=CLI_THEME, c_theme=CLI_THEME))
        elif output.status_code == 404:
            print(mdv(md="#Unable to find the requested resource", theme=CLI_THEME, c_theme=CLI_THEME))
        elif output.status_code >= 500:
            err = f"#Server Error \n" \
                f"> {output.url} - {output.status_code} - {output.text}"
            print(mdv(md=err, theme=CLI_THEME, c_theme=CLI_THEME))
        else:
            print(output.text)
    elif isinstance(output, str) and output.startswith('#'):
        print(mdv(md=output, theme=CLI_THEME, c_theme=CLI_THEME))
    else:
        print(str(output))


def display_version(package_name: str, md_file: str = 'VERSION.md'):
    md_path = Path(os.path.join(os.path.join(get_python_lib(), package_name), md_file))
    if os.path.exists(md_path):
        echo(mdv(filename=md_path))


def update_package(package_name: str, force: bool = False, pip_args: list = []):
    """Use this to expose a command to update your CLI.

    pip_args will be passed as a list to add things like trusted-host or extra-index-url.

    Example:
        pip_args = ['--extra-index-url', 'https://artifactory.com/api/pypi/eg/simple',
                    '--trusted-host', 'artifactory.com']

    :param package_name:
    :param force:
    :param pip_args:
    :return:
    """
    if force:
        proc = subprocess.Popen(
            ['pip3', 'uninstall', '-y', package_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output = proc.stdout.read().decode('utf-8')

    proc = subprocess.Popen(
        ['pip3', 'install', '--upgrade', package_name] + pip_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )

    return proc.stdout.read().decode('utf-8')


def ensure_latest_package(package_name: str, pip_args=[], md_file: str = 'VERSION.md', update_pkg_pip_args=[]):
    """Toss this in main to perform a check that the user is always running latest

    pip_args will be passed as a list to add things like trusted-host or extra-index-url.

    Example:
        pip_args = ['--extra-index-url', 'https://artifactory.com/api/pypi/eg/simple',
                    '--trusted-host', 'artifactory.com']

    :param package_name:
    :param pip_args:
    :param md_file: Display this file if the package was updated
    :param update_pkg_pip_args: pip args pass to update_package on out of date package e.g. --extra-index-url
    :return:
    """
    proc = subprocess.Popen(
        ['pip3', 'search', package_name] + pip_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = proc.stdout.read().decode('utf-8').replace(' ', '').split('\n')

    if len(output) > 1 and 'INSTALLED' in output[1] and 'latest' not in output[1]:
        update_pkg_pip_args = update_pkg_pip_args if update_pkg_pip_args else pip_args
        update_package(package_name, pip_args=update_pkg_pip_args)
        display_version(package_name, md_file)
        echo(f'#An update to {package_name} was retrieved that prevented your command from running.'
             f'\nPlease review changes and re-run your command.')
        sys.exit(0)
