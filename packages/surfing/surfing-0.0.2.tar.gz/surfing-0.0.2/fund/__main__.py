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
        print('data_download not implemented')

    def data_update(self):
        print('data_update not implemented')
    

if __name__ == "__main__":
    entrance = FundEntrance()
