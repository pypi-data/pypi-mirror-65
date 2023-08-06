import argparse
import sys

HELP_MSG = '''
surfing <command> [<args>]

The most commonly used commands are:
    init_raw                 setup raw database
    init_basic               setup basic database
    init_derived             setup derived database
    init_view                setup view database
'''

class SurfingEntrance(object):

    def __init__(self):
        parser = argparse.ArgumentParser(description='Fund Command Tool', usage=HELP_MSG)
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def _get_yesterday(self):
        import datetime
        yesterday = datetime.datetime.today() - datetime.timedelta(days = 1)
        yesterday_str = datetime.datetime.strftime(yesterday, '%Y%m%d')
        print(f'yesterday: {yesterday_str}')
        return yesterday_str

    def init_raw(self):
        from .data.wrapper.mysql import RawDatabaseConnector
        from .data.view.raw_models import Base

        print('Begin to create tables for database: raw')
        Base.metadata.create_all(bind=RawDatabaseConnector().get_engine())
        print('done')

    def init_basic(self):
        from .data.wrapper.mysql import BasicDatabaseConnector
        from .data.view.basic_models import Base

        print('Begin to create tables for database: basic')
        Base.metadata.create_all(bind=BasicDatabaseConnector().get_engine())
        print('done')

    def init_derived(self):
        from .data.wrapper.mysql import DerivedDatabaseConnector
        from .data.view.derived_models import Base

        print('Begin to create tables for database: derived')
        Base.metadata.create_all(bind=DerivedDatabaseConnector().get_engine())
        print('done')

    def init_view(self):
        from .data.wrapper.mysql import ViewDatabaseConnector
        from .data.view.view_models import Base

        print('Begin to create tables for database: view')
        Base.metadata.create_all(bind=ViewDatabaseConnector().get_engine())
        print('done')

    def download_raw(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()

        from .data.fund.raw.raw_data_downloader import RawDataDownloader
        from .util.config import SurfingConfigurator

        rq_license = SurfingConfigurator().get_license_settings('rq')
        raw_data_downloader = RawDataDownloader(rq_license)
        raw_data_downloader.download(yesterday, yesterday)
    
    def update_basic(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()

        from .data.fund.basic.basic_data_processor import BasicDataProcessor

        basic_data_processor = BasicDataProcessor()
        basic_data_processor.process_all(yesterday, yesterday)
    
    def update_derived(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()


    def update_view(self, yesterday=None):
        if not yesterday:
            yesterday = self._get_yesterday()


    def data_update(self):
        print('Start data update')

        yesterday = self._get_yesterday()

        print('Step 0. Start data download')
        self.download_raw(yesterday)
        print('Step 0. Done data download')

        print('Step 1. Start update basic')
        self.update_basic(yesterday)
        print('Step 1. Done update basic')

        print('Step 2. Start update derived')
        self.update_derived(yesterday)
        print('Step 2. Done update derived')
        
        print('Step 3. Start update view')
        self.update_view(yesterday)
        print('Step 3. Done update view')

        print('Done data update')
    

if __name__ == "__main__":
    entrance = SurfingEntrance()
