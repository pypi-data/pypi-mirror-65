import os
import json
import platform

from .helper import Singleton

DEFAULT_CONFIG_PATH = '/shared/surfing/config.json'
CURRENT_PLATFORM = platform.system()

class SysSettings(object):

    def __init__(self, sys_json):
        self.log_dir = sys_json.get('log_dir', '/shared/surfing/log/')
        self.temp_dir = sys_json.get('temp_dir', '/shared/surfing/temp/')  # 下载csv路径

        if CURRENT_PLATFORM == 'Darwin' or CURRENT_PLATFORM == 'Windows':
            curr_file_dir = os.path.split(os.path.realpath(__file__))[0]
            self.log_dir = curr_file_dir + '/../log/'
            self.temp_dir = curr_file_dir + '/../temp/'

        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)

    def get_temp_file_dir(self):
        return self.temp_dir

    def get_log_dir(self):
        return self.log_dir


class DbSettings(object):
    '''
    Parse database connection settings in config file
    '''
    def __init__(self, db_json):
        assert 'host' in db_json, 'could not find host in db settings'
        assert 'port' in db_json, 'could not find port in db settings'
        assert 'username' in db_json, 'could not find username in db settings'
        assert 'password' in db_json, 'could not find password in db settings'
        assert 'db' in db_json, 'could not find db in db settings'

        self.host = db_json['host']
        self.port = db_json['port']
        self.username = db_json['username']
        self.password = db_json['password']
        self.db = db_json['db']

    def to_conn_str(self):
        return 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            self.username, self.password, self.host, self.port, self.db
        )

    def __str__(self):
        return '<DB: {}@{}:{}/{}>'.format(self.username, self.host, self.port, self.db)


class HostSettings(object):

    def __init__(self, host_json):
        assert 'host' in host_json, 'could not find host in host_info settings'
        assert 'port' in host_json, 'could not find port in host_info settings'

        self.host = host_json['host']
        self.port = host_json['port']

    def to_dict(self):
        return {
            'host': self.host,
            'port': self.port,
        }

    def __str__(self):
        return '<HOSTING: {}@{}>'.format(self.host, self.port)


class SurfingConfigurator(metaclass=Singleton):

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        if CURRENT_PLATFORM == 'Darwin' or CURRENT_PLATFORM == 'Windows':
            curr_file_dir = os.path.split(os.path.realpath(__file__))[0]
            self.config_path = os.path.join(curr_file_dir, '../etc/config.json')
        self.config = json.load(open(self.config_path))

    def get_host_settings(self):
        assert 'hosting' in self.config, 'could not find hosting section in config'
        settings = HostSettings(self.config['hosting'])
        return settings

    def get_sys_settings(self):
        assert 'sys' in self.config, 'could not find sys section in config'
        settings = SysSettings(self.config['sys'])
        return settings

    def _get_db_settings(self, db_mode=None, key=None):
        assert key in self.config, 'could not find {} section in config'.format(key)
        db_info = db_mode or self.config[key].get('mode', 'developpment')
        assert db_info in self.config[key], 'could not find "{}" in config section'.format(db_info)
        db_section = self.config[key][db_info]
        settings = DbSettings(db_section)
        return settings

    def get_db_settings(self, db_mode=None, key=None):
        return self._get_db_settings(db_mode=db_mode, key=key)
