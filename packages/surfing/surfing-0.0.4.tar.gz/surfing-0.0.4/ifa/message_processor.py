from .message_receiver import WechatMessageReceiver
from .message_parser import WechatMessageParser
from .message_sender import WechatMessageSender
import time
import json
import urllib.parse
import sys
from .config import Configurator

class WechatMessageProcessor(object):

    def __init__(self):
        self.message_receiver = WechatMessageReceiver()
        self.message_parser = WechatMessageParser()
        self.message_sender = WechatMessageSender()

    def run(self):
        while True:
            time.sleep(0.01)

            message = self.message_receiver.get_message()
            if not message:
                continue
            
            result = self.message_parser.parse(message["msg_from"], message["msg_to"], message["msg_content"])

            # we can handle scenario 1 only
            if result['scenario_id'] == 1:
                target_url = 'http://52.82.113.3:12300/FundInfo?id='
                content = target_url + urllib.parse.quote_plus(result['param']['fund_id'])
            else:
                content = json.dumps(result)

            self.message_sender.send(message["msg_to"], content)

            #print(f'msg: ({message})\nresult: ({json.dumps(result)})\n')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        print(f'config path is set: {config_path}')
        Configurator(config_path).config_path = config_path
    wmp = WechatMessageProcessor()
    wmp.run()