from fund.db.database import DerivedDatabaseConnector,DerivedTestDatabaseConnector
from fund.util.logger import SurfingLogger
from fund.db.models import IndustryPE
from fund.util.utility import Utility

from .common import DataType
import datetime


class DataWriter(object):
    '''
    Data writer, which writes data in memory back to database
    (Memory) -> DataWriter -> (DB)
    '''

    def __init__(self):
        '''
        Initialization
        '''
        self._logger = SurfingLogger.get_logger(type(self).__name__)

    def write(self, data):
        '''
        Main function of DataWriter, to be called by DataEngine.
        :param data: data to be written to DB: {DataType->data}
        '''
        # Write data to FoF Database
        self._logger.info('Start writing data to db')
        output = {}
        data_write_targets = [
            [DataType.UPDATE_INDUSTRY_PE, 'positions'],
            [DataType.UPDATE_STOCK_ANNUAL_NET_PROFIT, 'new stock annual net profit'],
        ]
        for data_type, data_name in data_write_targets:
            if data_type in data:
                output[data_type] = []
                items = data[data_type]
                if type(items) != list:
                    self._logger.error(f'Data {data_name} to written is not list')

                if len(items) == 0:
                    continue
                
                self._logger.info(f'Start writing {data_name} to db')
                if self._write_derived_result(items):
                    self._logger.info(f'Done writing {data_name} to db')
                else:
                    self._logger.error(f'Failed to write {data_name} to db')

        return output

    def _write_derived_result(self, items):
        '''
        Write processed data back to DB
        :return: True for success, and False for failure
        '''
        self._logger.info(f'data len: {len(items)}')
        with DerivedDatabaseConnector().managed_session() as derived_session:
            try:
                derived_session.bulk_save_objects(items)
                derived_session.commit()
            except Exception as e:
                derived_session.rollback()
                self._logger.error(f'Write error <err>{e}')
                return False
        return True
