from .util import Singleton
import platform
import json

CURRENT_PLATFORM = platform.system()
DEFAULT_CONFIG_PATH = '/shared/etc/ifa/config.json'

class RedisSetting(object):

    def __init__(self, data_json):
        assert 'host' in data_json, 'could not find host in config file'
        assert 'port' in data_json, 'could not find port in config file'
        assert 'password' in data_json, 'could not find password in config file'
        assert 'key' in data_json, 'could not find key in config file'

        self.host = data_json['host']
        self.port = data_json['port']
        self.db = data_json.get('db', 0)
        self.password = data_json['password']
        self.key = data_json['key']

class MessageSenderSetting(object):

    def __init__(self, data_json):
        assert 'corp_id' in data_json, 'could not find corp_id in config file'
        assert 'app_id' in data_json, 'could not find app_id in config file'
        assert 'app_secret' in data_json, 'could not find add_secret in config file'

        self.corp_id = data_json['corp_id']
        self.app_id = data_json['app_id']
        self.app_secret = data_json['app_secret']

class Configurator(metaclass=Singleton):

    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        if CURRENT_PLATFORM == 'Darwin':
            import os
            curr_file_dir = os.path.split(os.path.realpath(__file__))[0]
            self.config_path = os.path.join(curr_file_dir, '../../etc/config.json')
        self.config = json.load(open(self.config_path))

    def get_redis_setting(self):
        settings = RedisSetting(self.config['redis'])
        return settings

    def get_message_sender_setting(self):
        settings = MessageSenderSetting(self.config['wxwork_app'])
        return settings
