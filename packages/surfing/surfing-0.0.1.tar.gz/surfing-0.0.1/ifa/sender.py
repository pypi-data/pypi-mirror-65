from .util import Singleton

class Sender(metaclass=Singleton):

    DRIVER_PATH = '/tool/chromedriver'
    ACCESS_TOKEN_URL = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'

    def __init__(self):
        message_sender_setting = Configurator().get_message_sender_setting()
        corp_id = message_sender_setting.corp_id
        app_secret = message_sender_setting.app_secret
        self.app_id = message_sender_setting.app_id
        self.access_token_snapshot = None
        self.access_token_expire_timestamp = None
        self.access_token_url = self.ACCESS_TOKEN_URL.format(corp_id, app_secret)

    def init(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--hide-scrollbars')
        self.driver = webdriver.Chrome(executable_path=self.DRIVER_PATH, options=options)
        width = 600
        height = 1150
        self.driver.set_window_size(width, height)
        self.driver.implicitly_wait(10)
    
    def get_access_token(self):
        now = datetime.datetime.now()
        if self.access_token_snapshot is None or now > self.access_token_expire_timestamp:
            res = requests.get(self.access_token_url, timeout=5)
            data = json.loads(res.text)
            if data['errcode'] != 0:
                print(f'Failed to get access token, errmsg: {data["errmsg"]}')
                self.access_token_snapshot = None
                return None
            self.access_token_snapshot = data['access_token']
            self.access_token_expire_timestamp = now + datetime.timedelta(seconds=data['expires_in']-30)
        return self.access_token_snapshot

    def capture_webpage(self, webpage_url):
        self.driver.get(webpage_url)
        time.sleep(0.8)
        # WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'tab-MONTH1')))
        print(f'b: {datetime.datetime.now()}')
        filename = f'/tmp/{webpage_url.split("/")[-1]}.png'
        self.driver.save_screenshot(filename)
        return filename

    def send(self, msg_to, msg_content):
        # Send snapshot of webpage and url
        # doc: https://open.work.weixin.qq.com/api/doc/90000/90135/90236
        access_token = self.get_access_token()
        target_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}'

        print(f'a: {datetime.datetime.now()}')
        
        filename = self.capture_webpage(msg_content)
        files = {'file': ('snapshot.png', open(filename, 'rb'), 'image/png', {'Expires': '0'})}

        print(f'c: {datetime.datetime.now()}')

        # upload image and get media_id
        # doc: https://open.work.weixin.qq.com/api/doc/90000/90135/90253
        upload_url = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image'
        res = requests.post(url=upload_url, files=files, timeout=30)
        data = json.loads(res.text)
        if data['errcode'] != 0:
            print(f'Failed to upload image, errmsg: {data["errmsg"]}')
            return
        media_id = data['media_id']

        print(f'd: {datetime.datetime.now()}')

        # Send image
        message = {
            'touser': msg_to,
            'msgtype': 'image',
            'agentid': self.app_id,
            'image' : {'media_id' : media_id}
        }
        res = requests.post(url=target_url, data=json.dumps(message), timeout=20)

        print(f'e: {datetime.datetime.now()}')

        # # Send url
        # message = {
        #     'touser': msg_to,
        #     'msgtype': 'text',
        #     'agentid': self.app_id,
        #     'text': {'content': msg_content}
        # }
        # res = requests.post(url=target_url, data=json.dumps(message), timeout=20)

        # print(f'e: {datetime.datetime.now()}')
