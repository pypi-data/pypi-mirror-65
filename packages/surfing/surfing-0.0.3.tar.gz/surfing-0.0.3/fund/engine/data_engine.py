import time
import signal
import datetime
import threading

from fund.util.timer import Timer
from fund.util.logger import SurfingLogger

from .common import DataType
from .data_loader import DataLoader
from .data_processor import DataProcessor
from .data_writer import DataWriter
from .dp_modules.pe_module import PeDailyModule

class DataEngine_test(object):
    '''
    Data engine consists of 3 parts, and schedules the data and work:
    1. DataLoader: load data from DB to memory
    2. DataProcessor: do the calculating using data in memory
    3. DataWriter: write data from memory to database
    DataLoader -> DataProcessor -> DataWriter
    '''

    def __init__(self):
        '''
        Initialization
        '''
        self._logger = SurfingLogger.get_logger(type(self).__name__)

        # Last data load timestamp, None if never
        self._data = {}

        # Data loader used to load database
        self._data_loader = DataLoader()

        # Data processor
        self._data_processor = DataProcessor()

        # Attach data processing modules to data_processor
        self._data_processor.attach(0, PeDailyModule())
        # self._data_processor.attach(0, TransactionModule())
        # self._data_processor.attach(0, UsdtPriceModule())
        # self._data_processor.attach(1, PerformanceModule())
        # self._data_processor.attach(2, RiskModule())
        # self._data_processor.attach(3, RiskEventModule())

        # Data writer
        self._data_writer = DataWriter()

        # Interrupt signal
        self._received_signal = None

    def _signal_handler(self, signum=None, frame=None):
        '''
        Handle interrupt signals
        '''
        if self._received_signal is None:
            self.stop(signum=signum)

    def start(self):
        '''
        Start data engine
        '''
        # Register Interrupt handler
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

        # Start data engine
        time_interval_seconds = 60*60*24
        th = threading.Thread(
            target=self._run_periodic_task,
            args=[time_interval_seconds])
        th.setDaemon(True)
        th.start()

        while True:
            time.sleep(0.1)
            if self._to_stop():
                break

    def stop(self, signum=signal.SIGTERM):
        '''
        Stop data engine
        '''
        self._logger.info('Stopping, please wait...')
        self._received_signal = signum
        self._on_stop()

    def _on_stop(self):
        '''
        Called before stopping, could be used to save data
        '''
        self._logger.warn('Data engine is going to stop!')

    def _to_stop(self):
        '''
        Whether data engine needs to be stopped
        '''
        return self._received_signal is not None

    def _run_periodic_task(self, time_interval_seconds):
        '''
        Run periodic task
        :param time_interval_seconds: time interval of periodic tasks
        '''
        if time_interval_seconds is None or time_interval_seconds < 0:
            self._logger.error(f'Invalid time interval <time_interval_seconds> {time_interval_seconds}')
            self.stop()

        last_start = None
        while not self._to_stop():
            now = datetime.datetime.now()
            today = datetime.datetime.combine(now.date(), datetime.time())
            delta = (now - today).seconds
            now = today + datetime.timedelta(seconds=delta)
            residual = delta % time_interval_seconds

            next_start = None
            if last_start is None:
                if residual != 0:
                    time_to_sleep = time_interval_seconds - residual
                    if time_to_sleep > 2:
                        time_to_sleep /= 2
                    time.sleep(time_to_sleep)
                    continue
                else:
                    next_start = now
            else:
                next_start = last_start + datetime.timedelta(seconds=time_interval_seconds)
            self._logger.info(f'now: {now}, next_start: {next_start}')
            if now >= next_start:
                try:
                    calculate_daily = delta < time_interval_seconds
                    if last_start is not None:
                        last_start_nano = Timer.time_to_nano(last_start.timestamp())
                    else:
                        last_start_nano = None

                    self._run_task(
                        last_start_nano=last_start_nano,
                        curr_nano=Timer.time_to_nano(next_start.timestamp()),
                        calculate_daily=calculate_daily
                    )
                except Exception as e:
                    self._logger.error(f'Periodic task execution error <err_msg>{e}')
                last_start = next_start
            else:
                time_to_sleep = time_interval_seconds - residual
                if time_to_sleep > 2:
                    time_to_sleep /= 2
                time.sleep(time_to_sleep)
                continue

    def _run_task(self, last_start_nano=None, curr_nano=None, calculate_daily=None):
        self._logger.info('Start to run task')

        # Load initial data from database
        data_loaded = self._data_loader.load(start_time=last_start_nano, end_time=curr_nano, date=calculate_daily, internal_data=self._data)
        # TODO: merge data_loaded and self._data, not just assignment!
        self._data.update(data_loaded)
        # self._data[DataType.CALCULATE_DAILY] = calculate_daily
        self._logger.info('Start to process')
        # Run data processing
        status = self._data_processor.process(self._data)

        if not status:
            self._logger.error('Error in data_processor')

        # Write processed data back to database, and clear output data buffer
        data_writer_output = self._data_writer.write(self._data)
        self._data.update(data_writer_output)


if __name__ =='__main__':
    a = DataEngine_test()
    a._run_task(calculate_daily='20190201')