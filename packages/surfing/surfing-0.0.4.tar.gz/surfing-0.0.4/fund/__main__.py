import argparse
import sys

HELP_MSG = '''
fof <command> [<args>]

The most commonly used commands are:
    init_raw                 setup raw database
    init_basic               setup basic database
    init_derived             setup derived database
    init_view                setup view database
'''

class FundEntrance(object):

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
        from .db.database import RawDatabaseConnector
        from .db.raw_models import Base

        print('Begin to create tables for database: raw')
        Base.metadata.create_all(bind=RawDatabaseConnector().get_engine())
        print('done')

    def init_basic(self):
        from .db.database import BasicDatabaseConnector
        from .db.basic_models import Base

        print('Begin to create tables for database: basic')
        Base.metadata.create_all(bind=BasicDatabaseConnector().get_engine())
        print('done')

    def init_derived(self):
        from .db.database import DerivedDatabaseConnector
        from .db.derived_models import Base

        print('Begin to create tables for database: derived')
        Base.metadata.create_all(bind=DerivedDatabaseConnector().get_engine())
        print('done')

    def init_view(self):
        from .db.database import ViewDatabaseConnector
        from .db.view_models import Base

        print('Begin to create tables for database: view')
        Base.metadata.create_all(bind=ViewDatabaseConnector().get_engine())
        print('done')

    def data_download(self):
        print('Start data download')
        from .downloader.raw_data_downloader import RawDataDownloader
        from .util.config import SurfingConfigurator
        rq_license = SurfingConfigurator().get_license_settings('rq')
        raw_data_downloader = RawDataDownloader(rq_license)
        yesterday = self._get_yesterday()
        raw_data_downloader.download(yesterday, yesterday)
        print('Done data download')

    def data_update(self):
        print('Start data update')

        print('Step 1. Start update basic')
        from .data_processor.basic.basic_data_processor import BasicDataProcessor
        basic_data_processor = BasicDataProcessor()
        yesterday = self._get_yesterday()
        basic_data_processor.process_all(yesterday, yesterday)
        print('Step 1. Done update basic')

        print('Done data update')
    

if __name__ == "__main__":
    entrance = FundEntrance()
