from .processor import IfaProcessor
from .struct import WxMsgItem

class FundProcessor(IfaProcessor):

    def __init__(self):
        pass

    def process(self, msg: WxMsgItem):
        if msg.msgtype == 'text':