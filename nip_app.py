"""nip

Usage:
    nip init (py|js) [--python=<python>] [--pip=<pip>] [--npm=<npm>] <name>
    nip run
    nip shell
    nip install
    nip install [--dev] <package>...
    nip clean [--full] [--migrations]
    nip migrate <app>
    nip help

Options:
    -h --help           Show this screen.
    --python=<python>   Python version [default: python3].
    --js                JavaScript Version.
    --pip=<pip>         Pip version [default: pip3].
    --npm=<npm>         NpM version.
    --version           Show version.
    --dev               Install as dev dependency.
    --migrations        Remove all migrations.
    --full              Remove all and reinstall."""

import sys
import os
import subprocess
import shlex
import json

pwd = os.getcwd()
niptemp = open('.niptemp', 'w')
print('cd ../\nls', file=open('.niptemp', 'w+'))

project_settings = {
    'language': '',
    'languageVersion': '',
    'installer': '',
}


class ToolNotInstalled(Exception):
    pass


def run_ext_cmd(*ar):
    for a in ar:
        print(a, file=niptemp)


def run_cmd(cmd):
    return str(subprocess.run(shlex.split(cmd), stdout=subprocess.PIPE).stdout)


try:
    from docopt import docopt
except ImportError:
    pip = 'pip3'
    for arg in sys.argv:
        if '--pip' in arg:
            pip = '='.split(arg)[1]

    run_cmd('%s install docopt' % pip)
    from docopt import docopt


args = docopt(__doc__, version='nip 0.0.1')
print(args)


def is_tool(name):
    """Check whether `name` is on PATH and marked as executable."""
    from shutil import which

    return which(name) is not None


def init_python(project_name):
    global project_settings

    if not is_tool('virtualenv'):
        print('Plz install virtualenv')
        print('%s install virtualenv' % args['<pip>'])
        raise ToolNotInstalled

    python = args['--python']

    if not is_tool(python):
        print('%s is not installed in your system' % python)
        raise ToolNotInstalled

    run_ext_cmd('virtualenv venv --python=%s' % python)

    # Activate external venv
    run_ext_cmd('. venv/bin/activate')
    run_ext_cmd('touch requirements.txt')

    # Clear external console
    run_ext_cmd('clear')

    # Get external output
    run_ext_cmd('echo Started %s project %s' % (python, project_name))

    project_settings = {
        'language': 'py',
        'languageVersion': run_cmd('python --version'),
        'installer': 'pip',
    }


def handel_init():
    """Handel the `init` command"""
    global project_settings

    try:
        project_name = args['<name>']

        command_on_error = ''
        if project_name == '.':
            project_dir = pwd
        else:
            project_dir = os.path.join(pwd, project_name)
            run_cmd('mkdir %s' % project_dir)

            # `cd` inside subprocess and in external shell too.
            run_ext_cmd('cd %s' % project_dir)
            run_cmd('cd %s' % project_dir)
            command_on_error = 'rm -rf %s' % project_dir

        try:
            if sys.argv[2] == 'py':
                init_python(project_name)
            else:
                print('See help for available project types')
                exit(1)
        except ToolNotInstalled:
            run_cmd(command_on_error)
            exit(1)

        settings_file_path = os.path.join(project_dir, 'nip.json')
        print(json.dumps(project_settings), file=open(settings_file_path, 'w+'))

    except IndexError:
        print('Specify project type')


def handel_help():
    print(__doc__)


def main():
    print(sys.argv)
    try:
        {
            'init': handel_init,
            'help': handel_help
        }[sys.argv[1]]()
    except IndexError:
        print('Index error')
        handel_help()
        exit(1)
    except KeyError as key_error:
        print(key_error)
        print('Command not supported')
        exit(1)

    exit(0)


main()
