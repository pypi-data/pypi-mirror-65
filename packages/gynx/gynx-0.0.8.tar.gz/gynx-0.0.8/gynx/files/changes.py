#!/usr/bin/python3.6

import os
import shutil
import sys
import time
import logging
from watchdog.observers import Observer
from gynx.core import log
from gynx.files.events.handlers import GynxEventHandler


class Changes:
    '''
    Base changes class (initialization only)
    '''

    def __init__(self, gynx, cache=None, testing=False, duration=None, *args, **kwargs):
        self.gynx = gynx
        self.service = gynx.service
        self.cache = cache
        self.testing = testing
        self.duration = duration
        self.logger = logging.getLogger('gynx.files.changes')


class RemoteChanges(Changes):
    '''
    Remote changes monitor class. Get static changes or watch real-time.
    '''

    def get(self):
        '''
        Full list of changes to remote file system.
        '''
        #fields = 'nextPageToken, changes(time, removed)'
        fields = '*'
        ptr = self.service.changes().getStartPageToken().execute()
        page_token = ptr['startPageToken']
        changes = []
        while page_token is not None:
            response = self.service.changes().list(
                pageToken=page_token, spaces='drive', fields=fields
            ).execute()
            for change in response.get('changes'):
                changes.append(change)
                log(
                    message='Change found for file: %s' % change.get('fileId'),
                    method=self.logger.info
                )
            page_token = response.get('nextPageToken')
        return changes

    def watch(self):
        '''
        Watch for real time changes to the remote drive (currently unsupported)
        '''
        fields = 'nextPageToken, changes(time, removed)'
        ptr = self.service.changes().getStartPageToken().execute()
        page_token = ptr['startPageToken']
        changes = []
        while page_token is not None:
            response = self.service.changes().watch(
                pageToken=page_token, spaces='drive', fields=fields, body={}
            ).execute()
            log(message=response, method=self.logger.info)


class LocalChanges(Changes):
    '''
    Local file changes monitor class. Watch and handle local filesystem changes
    using the watchdog library. Captured events are passed to the event handler
    to be parsed and executed accordingly.
    '''

    def __init__(self, rootdir, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rootdir=rootdir
        self.observer = Observer()
        self.event_handler = GynxEventHandler(
            gynx=self.gynx, cache=self.cache, rootdir=self.rootdir
        )

    def test_changes(self, count):
        '''
        On a testing run, create, edit, move and delete some sample files and
        folders to initiate some test event captures.
        '''
        testfolderpath = os.path.join(self.rootdir, 'testfolder')
        testfilepath = os.path.join(self.rootdir, 'testfile.txt')
        newfilepath = os.path.join(testfolderpath, 'testfile.txt')
        if count == 1:
            os.mkdir(testfolderpath)
            with open(testfilepath, 'w') as testfile:
                testfile.write('test text.')
        if count == 2:
            with open(testfilepath, 'a') as testfile:
                testfile.write('more text.')
        if count == 3:
            os.rename(testfilepath, newfilepath)
        if count == 4:
            os.remove(newfilepath)
            try:
                shutil.rmtree(testfolderpath)
            except OSError:
                pass
        if count > 5:
            raise KeyboardInterrupt

    def watch(self):
        '''
        Monitor the local filesystem for changes for a configurable duration.
        '''
        log(
            message='Starting local file monitoring...',
            method=self.logger.info
        )
        path = self.rootdir if os.path.exists(self.rootdir) else '.'
        self.observer.schedule(self.event_handler, path, recursive=True)
        self.observer.start()
        count = 0
        try:
            while True:
                time.sleep(1)
                count += 1
                if self.testing:
                    self.test_changes(count)
                if self.duration:
                    if count > self.duration * 60:
                        raise KeyboardInterrupt
        except KeyboardInterrupt:
            log(
                message='Stopping local file monitoring...',
                method=self.logger.info
            )
            self.observer.stop()
        self.observer.join()
