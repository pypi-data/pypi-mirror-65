class WechatMessageParser(object):

    def parse(self, msg_from, msg_to, msg_content):
        result = {}
        result['scenario_id'] = 1
        result['param'] = {'fund_id': msg_content}
        return result