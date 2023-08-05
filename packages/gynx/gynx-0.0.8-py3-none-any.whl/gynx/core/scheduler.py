import schedule
import time
from datetime import datetime, timedelta
import logging

class GynxScheduler:
    '''Run gynx commands on a schedule'''

    def __init__(self, duration=10, days=None, hours=None, *args, **kwargs):
        '''
        Initialize scheduler class with a set duration/interval between app
        executions and optional days/hours arguments to stop execution
        '''
        self.duration = duration
        self.days = days
        self.hours = hours
        self.logger = logging.getLogger('gynx.core.scheduler')

    def add_job(self, callback):
        '''
        Add jobs to the scheduler at the predefined intervals
        '''
        schedule.every(self.duration).minutes.do(callback)

    def start(self):
        '''
        Start the scheduled jobs execution
        '''
        start_time = datetime.now()
        if self.days and self.hours:
            end_time = start_time + timedelta(days=self.days, hours=self.hours)
        elif self.days:
            end_time = start_time + timedelta(days=self.days)
        elif self.hours:
            end_time = start_time + timedelta(hours=self.hours)
        while True:
            schedule.run_pending()
            if self.days or self.hours:
                if datetime.now() >= end_time:
                    return
            time.sleep(1)
