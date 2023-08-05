import sys
import json
import datetime
import requests
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class NotifyMaster:

    WX_MSG_URL = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c631aba2-6d24-4fc0-9dfd-d5ae6311baea'

    @staticmethod
    def send_msg(job_id:str='',source:str='',content:str='', is_error:bool=False):
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')        
        status_msg  =   '<font color="red">FAILED</font>' if is_error else '<font color="green"> SUCCESS</font>' 
        msg_data = {
            'msgtype'       :   'markdown',
            'markdown'      :   {
                'content'   :   ''' >**程序信息** 
                                    >序号：<font color="gray">job_id : {}</font>
                                    >来源：<font color="blue">{}</font>  
                                    >时间：<font color="yellow">{}</font> 
                                    >状态：{}
                                    >信息：<font color="black">{}</font>
                                   '''.format(job_id, source, time_now, status_msg, content),
            },
        }    
        res = requests.post(url=NotifyMaster.WX_MSG_URL, json=msg_data)

class MSG:

    def __init__(self,job_id=None,source=None):
        self.source = source
        self.job_id = job_id
        self.msg_id = 0

    def send(self, content, is_error, chat_con):
        content = "__{}__\n'{}'".format(self.msg_id, content)
        logger.info(content)    
        if chat_con:
            NotifyMaster.send_msg(job_id=self.job_id, source=self.source, content = content, is_error=is_error)
            self.msg_id += 1
    