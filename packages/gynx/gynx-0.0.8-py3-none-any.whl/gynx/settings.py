## GYNX settings ##
import os
import logging

# Set environment
ENVIRONMENT = 'master'

live = True if ENVIRONMENT == 'live' or ENVIRONMENT == 'master' else False

# Base settings variables (environment specific)

class Settings:

    def __init__(self, environment, *args, **kwargs):
        self.environment = environment

    @property
    def DEBUG(self):
        return False if self.environment == 'live' else True

    @property
    def DIRECTORY(self):
        testdrive = os.path.join(os.getcwd(), 'tests', 'drive/')
        return os.getcwd() + '/' if self.environment == 'live' else testdrive

    @property
    def TOKEN_FILE(self):
        return 'token.json' if self.environment == 'live' else 'test.json'

    class Logging:

        def __init__(self, *args, **kwargs):
            self.directory = os.path.join(os.path.expanduser('~'), '.gynx')
            self.logfile = os.path.join(self.directory, 'gynx.log')
            if not os.path.exists(self.directory):
                os.mkdir(self.directory)

        def setup(self):
            # Disable Google API and schedule logs
            google_api_logger = logging.getLogger('googleapiclient.discovery')
            google_api_logger.propagate = False
            schedule_logger = logging.getLogger('schedule')
            schedule_logger.propagate = False
            # Set up debug level file logging
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                filename=self.logfile,
                filemode='w'
            )
            # Set up info level console logging
            console = logging.StreamHandler()
            console.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(name)-12s: %(levelname)-8s %(message)s'
            )
            console.setFormatter(formatter)
            self.logger = logging.getLogger('')
            self.logger.addHandler(console)

test_environment = Settings('test')
live_environment = Settings('live')

environment = live_environment if live else test_environment
