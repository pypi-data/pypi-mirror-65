#!/usr/bin/python3.6

from gynx.settings import environment as settings
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools
from datetime import datetime
import pytz
import os
import sys
import logging

SCOPES = 'https://www.googleapis.com/auth/drive'

def log(message, method=None):
    '''
    Print messages to console with logger, if available, or sys.stdout, while
    preventing printing from the
    '''
    if method:
        method(message)
    else:
        sys.stdout.write('%s\n' % message)


class Gynx():

    def __init__(self, quiet=False, debug=False, *args, **kwargs):
        '''
        Initialize by building Drive service with provided credentials.
        '''
        self.root = settings.DIRECTORY
        self.appdir = os.path.dirname(
            os.path.dirname(os.path.realpath(__file__))
        ) + '/'
        self.start = datetime.now().replace(tzinfo=pytz.UTC)
        self.quiet = quiet
        self.debug = debug
        creds = self.get_credentials()
        self.service = discovery.build(
            'drive',
            'v3',
            http=creds.authorize(Http()),
            cache_discovery=False
        )
        self.logger = logging.getLogger('gynx.core')

    def __str__(self):
        return 'gynx initialized at %s' % str(self.start)

    def get_credentials(self):
        '''
        Authenticate via user token combined with gynx app API credentials.
        Token generated initially after in-browser authorisation.
        '''
        store = file.Storage(
            self.appdir + 'credentials/%s' % settings.TOKEN_FILE
        )
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                self.appdir + 'credentials/credentials.json',
                SCOPES
            )
            creds = tools.run_flow(flow, store)
        return creds

    def get_info(self):
        '''
        Information about the Drive user and library storage limits/usage.
        '''
        return self.service.about().get(fields='user, storageQuota').execute()

    def print_info(self):
        '''
        Print user information and calculate usage percentage.
        '''
        info = self.get_info()
        name = info['user']['displayName']
        sys.stdout.write('Name: %s\n' % name)
        usage = float(info['storageQuota']['usage'])
        sys.stdout.write('Usage: %s\n' % self.print_size(int(usage)))
        limit = float(info['storageQuota']['limit'])
        sys.stdout.write('Limit: %s\n' % self.print_size(int(limit)))
        used = float((usage/limit)*100)
        sys.stdout.write('Used: %s%%\n' % str(round(used, 2)))

    def print_size(self, bytes):
        '''
        Clean print file size in GB, MB, KB or B based on size
        '''
        if bytes >= 1000000000:
            return '{0:.2f}'.format(float(bytes)/1000000000.0) + ' GB'
        if bytes >= 1000000:
            return '{0:.2f}'.format(float(bytes)/1000000.0) + ' MB'
        if bytes >= 1000:
            return '{0:.2f}'.format(float(bytes)/1000.0) + ' KB'
        return str(bytes) + ' B'
