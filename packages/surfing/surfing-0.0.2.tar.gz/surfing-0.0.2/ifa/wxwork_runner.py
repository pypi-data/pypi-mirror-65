
from .config import Configurator
from .struct import WxRawData, WxSeqItem, WxMsgItem
from .processor import IfaProcessor
import time, json

import sys
sys.path.append('/shared/build_surfing/src')
import libwxwork

class WxworkRunner(object):

    def __init__(self, seq=None):
        self.seq = seq
        corp_id = Configurator().config['wxwork']['corp_id']
        secret_key = Configurator().config['wxwork']['secret_key']
        private_key = Configurator().config['wxwork']['private_key']
        self.wrapper = libwxwork.WxworkWrapper(corp_id, secret_key, private_key, -1)
        self.processors = []

    def register(self, processor: IfaProcessor):
        self.processors.append(processor)

    def run(self):
        print(self.wrapper.init())
        self.seq = self.seq or 0
        while True:
            time.sleep(1)
            res = self.wrapper.get(self.seq, 500)
            #try:
            data = WxRawData(**json.loads(res))
            for item in data.chatdata:
                self.process(item)
            self.seq = data.max_seq or self.seq
            print(data)

    def process(self, item: WxSeqItem):
        decrypted = None
        try:
            decrypted_str = self.wrapper.decode(item.encrypt_random_key, item.encrypt_chat_msg)
            decrypted = json.loads(decrypted_str)
        except:
            print('!' * 10)
            print(f'error: {decrypted_str}')
            print('!' * 10)
        if decrypted:
            msg = WxMsgItem(decrypted)
            for pr in self.processors:
                self.processors.process(msg)
            print(msg)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        config_path = sys.argv[1]
        print(f'config path is set: {config_path}')
        Configurator(config_path).config_path = config_path
        if len(sys.argv) > 2:
            seq = int(sys.argv[2])
    wmp = WxworkRunner(seq)
    wmp.run()