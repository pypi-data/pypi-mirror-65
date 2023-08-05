#!/usr/bin/python3.6

import sys
import os
import subprocess
import argparse
from textwrap import dedent

VERSION = '0.0.8'

NAME = 'gynx'

DESCRIPTION = 'Google Drive sync client for Linux'

USAGE = '''
gynx  [-V|--version] [-h|--help] [-v[v[v]]|--verbose]
      [-c|--clean] [-r|--refresh] [-a|--auth] [-d|--dry-run]
      [-s|--schedule] [-D|--duration <minutes>] [-S|--start]
'''

OPTIONS = '''
-V --version      show gynx version and exit
-h --help         show this help message and exit
-v --verbose      print additional output during run
-c --clean        clear file cache before run
-r --refresh      delete contents of local drive before run
-a --auth         renew authentication token before run
-d --dry-run      print operations without execution
-s --schedule     run sync automatically on a schedule
-D --duration     minutes until next automatic sync (default 60)
-S --start        start automatic folder monitoring
'''

INFO = 'NAME\n\n  %s\n\nDESCRIPTION\n\n  %s\n\nUSAGE\n\n  %s\n\nOPTIONS\n\n  %s' % (
    NAME, DESCRIPTION, USAGE, OPTIONS
)


class GynxRunner(object):

    def __init__(self, *args, **kwargs):
        '''
        Initialize runner class with arguments parsed from the bash entrypoint.
        '''
        parser = argparse.ArgumentParser(
            prog='gynx',
            description=DESCRIPTION,
            usage=USAGE
        )
        parser.add_argument(
            '-V', '--version', action='version', version=VERSION
        )
        parser.add_argument(
            '-v', '--verbose', dest='verbose', action='count',
            help='print additional output during run'
        )
        parser.add_argument(
            '-c', '--clean', dest='clean', action='store_true',
            help='clear file cache before run'
        )
        parser.add_argument(
            '-r', '--refresh', dest='refresh', action='store_true',
            help='delete contents of local drive before run'
        )
        parser.add_argument(
            '-a', '--auth', dest='auth', action='store_true',
            help='renew authentication token before run'
        )
        parser.add_argument(
            '-d', '--dry-run', dest='dry', action='store_true',
            help='print operations without execution'
        )
        parser.add_argument(
            '-s', '--schedule', dest='schedule', action='store_true',
            help='run sync automatically on a schedule'
        )
        parser.add_argument(
            '-D', '--duration', dest='duration', default=10, metavar='',
            type=int, help='minutes until next automatic sync (default 60)'
        )
        parser.add_argument(
            '-S', '--start', dest='start', action='store_true',
            help='start automatic folder monitoring'
        )
        self.options = parser.parse_args()
        self.create_cache()

    def log(self, message):
        '''
        Print messages to console with sys.stdout and prevent other printing
        '''
        sys.stdout.write('%s\n' % message)

    @property
    def appdir(self):
        '''
        Attempt to import gynx project to locate and return the environment path.
        If the project can't be imported, a development environment is assumed
        and the directory at ../gynx/ from the script location is returned.
        '''
        try:
            import gynx
            appdir = gynx.__path__[0]
        except ImportError:
            appdir = os.path.join(
                os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
                'gynx'
            )
        if os.path.isdir(appdir):
            return appdir
        else:
            self.log('%s is not a valid directory' % appdir)
            sys.exit()

    def create_cache(self):
        '''
        Create CACHE folder inside the app directory for storing JSON state.
        '''
        appdir = self.appdir
        if not os.path.isdir(os.path.join(appdir, 'CACHE')):
            os.mkdir(os.path.join(appdir, 'CACHE'))

    def execute(self, commands):
        '''
        Execute a list of shell commands using subprocess.call
        '''
        for command in commands:
            subprocess.call(command, shell=True)

    def clean(self):
        '''
        Remove JSON files in CACHE folder if they exist
        '''
        if os.path.exists(os.path.join(self.appdir, 'CACHE', 'remote.json')):
            self.log('Clearing remote cache...')
            os.remove(os.path.join(self.appdir, 'CACHE', 'remote.json'))
        if os.path.exists(os.path.join(self.appdir, 'CACHE', 'local.json')):
            self.log('Clearing local cache...')
            os.remove(os.path.join(self.appdir, 'CACHE', 'local.json'))

    def refresh(self):
        '''
        Delete the contents of the local directory after user confirmation.
        Clean files in CACHE first if -c|--clean flag not also specified.
        '''
        confirm = input(dedent('''
            This will delete the contents of your current directory.
            Are you sure you want to continue? (y/n):
        '''))
        if confirm.upper() == 'Y':
            if not self.options.clean:
                self.clean()
            self.log('Deleting local directory contents...')
            self.execute(['rm -rv %s/*' % os.getcwd()])

    def authorize(self):
        '''
        Delete token.json and allow the user to re-authorize
        '''
        token_file = os.path.join(self.appdir, 'credentials', 'token.json')
        if os.path.exists(token_file):
            self.log('Clearing authenticaton token...')
            os.remove(token_file)

    def start(self, arguments):
        '''
        Run app.py with parsed arguments
        '''
        if os.path.exists(os.path.join(self.appdir, 'app.py')):
            app = os.path.join(self.appdir, 'app.py')
            command = 'python "%s" %s' % (app, arguments)
            self.execute([command])

    def run(self):
        '''
        Run functions based on arguments and pass remaining arguments to app.py
        '''
        arguments = []
        if self.options.verbose:
            arguments.append('verbose')
            if self.options.verbose > 1:
                arguments.append('extra_verbose')
            if self.options.verbose > 2:
                arguments.append('super_verbose')
        if self.options.clean:
            self.clean()
        if self.options.refresh:
            self.refresh()
        if self.options.auth:
            self.authorize()
        if self.options.dry:
            arguments.append('dry')
        if self.options.schedule:
            arguments.append('schedule')
            arguments.append(str(self.options.duration))
        if self.options.start:
            arguments.append('start')
        self.start(' '.join(arguments))

runner = GynxRunner()
runner.run()
