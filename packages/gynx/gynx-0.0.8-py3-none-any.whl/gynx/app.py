#!/usr/bin/python3.6

from gynx.settings import environment as settings
from gynx.core import Gynx, log
from gynx.core.scheduler import GynxScheduler
from gynx.files.readers import *
from gynx.files.differences import *
from gynx.files.operations import *
from gynx.files.changes import *
import logging

class GynxApp(object):
    '''
    Core app class to define and run the main program thread.
    '''

    def __init__(
        self,
        verbose=False,
        dry_run=False,
        schedule=False,
        start=False,
        testing=False
    ):
        '''
        Initialize app class with parameters that can overwrite CLI arguments
        '''
        self.gynx = None
        self._verbose = verbose
        self._dry_run = dry_run
        self._schedule = schedule
        self._start = start
        self.testing = testing
        self.logging = settings.Logging()
        self.logging.setup()
        self.logger = logging.getLogger('gynx.app')

    @property
    def verbose(self):
        '''
        Print additional output to console during app execution
        '''
        verbosity = 0
        if 'verbose' in sys.argv or settings.DEBUG or self._verbose:
            verbosity = 1
            if 'extra_verbose' in sys.argv:
                verbosity = 2
                if 'super_verbose' in sys.argv:
                    verbosity = 3
        return verbosity

    @property
    def dry_run(self):
        '''
        Print the operations to be performed to the console, but don't run them
        '''
        return 'dry' in sys.argv or self._dry_run

    @property
    def schedule(self):
        '''
        Start the app execution on a schedule (default 10 minute intervals)
        '''
        return 'schedule' in sys.argv or self._schedule

    @property
    def duration(self):
        '''
        Duration for the app schedule, if present
        '''
        if self.schedule or self.start:
            si = sys.argv.index('schedule') if 'schedule' in sys.argv else None
            return int(sys.argv[si+1]) if si else 10
        return None

    @property
    def start(self):
        '''
        Start continuous monitoring in between scheduled executions
        '''
        return 'start' in sys.argv or self._start

    def run(self):
        '''
        Run program thread:
            1. gynx.core                initialize and authenticate
            2. gynx.files.readers       read local and remote directories
            3. gynx.files.differences   parse differences between directories
            4. gynx.files.operations    run sync operations
        '''
        gynx = Gynx(quiet=True if not self.verbose else False)
        self.gynx = gynx
        if self.verbose > 1:
            log(message=str(gynx), method=self.logger.info)
            gynx.print_info()
        local_reader = LocalFileReader(
            src=gynx.appdir,
            rootdir=gynx.root,
            quiet=gynx.quiet
        )
        local = local_reader.files
        remote_reader = RemoteFileReader(
            src=gynx.appdir,
            service=gynx.service,
            info=gynx.get_info(),
            quiet=gynx.quiet
        )
        remote = remote_reader.files
        differences = Differences(
            remote_files=remote,
            local_files=local,
            previous=remote_reader.load(),
            root=gynx.root,
            initial=remote_reader.initial
        )
        if self.dry_run:
            differences.print_all()
        else:
            operations = SyncOperations(
                service=gynx.service,
                changes=differences.all(),
                remote=remote,
                local=local,
                root=gynx.root,
                rf=remote_reader.remote_folders
            )
            operations.run()
            if self.start:
                local_changes = LocalChanges(
                    gynx=gynx,
                    rootdir=gynx.root,
                    duration=self.duration-0.1,
                    cache=remote
                )
                if not self.testing:
                    local_changes.watch()

    def execute(self):
        if self.schedule or self.start:
            log(
                message='Running sync every %d minute%s' % (
                    self.duration, 's' if self.duration != 1 else ''
                ),
                method=self.logger.info
            )
            self.run()
            scheduler = GynxScheduler(
                duration=self.duration,
                hours=self._schedule
            )
            scheduler.add_job(self.run)
            if not self.testing:
                try:
                    scheduler.start()
                except KeyboardInterrupt:
                    sys.exit()
        else:
            self.run()

def main():
    app = GynxApp()
    app.execute()

if __name__ == '__main__':
    main()
