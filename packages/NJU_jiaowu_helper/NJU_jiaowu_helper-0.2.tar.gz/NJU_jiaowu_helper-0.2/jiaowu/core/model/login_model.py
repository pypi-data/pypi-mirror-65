from src.core.function.utils.others import recognize_captcha
from src.data.config.login_config import login_headers

import requests


class LoginInitializer:
    def __init__(self,username=None,password=None):
        self.username = username
        self.passwd = password

    def set_username(self, username):
        self.username = username

    def set_passwd(self, pwd):
        self.passwd = pwd

    # 登录
    def _login(self, captcha, cookie):
        target_url = "http://elite.nju.edu.cn/jiaowu/login.do"
        post_data = {'userName': self.username, 'password': self.passwd, 'returnUrl': 'null', 'ValidateCode': captcha}
        headers = login_headers
        response = requests.post(url=target_url, data=post_data, headers=headers, cookies=cookie)
        response_cookies = response.cookies
        # print(cookies)
        return response_cookies

    def start_session(self):
        # 由于识别正确率低，暂时用循环的方法直到识别正确
        cookies = None
        while True:
            # 完整的获取验证码登录过程
            response = requests.get(url="http://elite.nju.edu.cn/jiaowu/ValidateCode.jsp")
            cookies1 = response.cookies
            cookies1_dict = requests.utils.dict_from_cookiejar(cookies1)
            captcha_save_path = "../data/output/raw_captcha.png"
            with open(captcha_save_path, "wb") as f:
                f.write(response.content)
            # 识别验证码
            result = recognize_captcha(captcha_save_path)
            # print(result)
            cookies2 = self._login(result, cookies1)
            cookies2_dict = requests.utils.dict_from_cookiejar(cookies2)

            # 识别正确
            if len(cookies2_dict) > 0:
                # 合并cookie
                cookies_dict = dict(cookies1_dict, **cookies2_dict)
                cookies = requests.utils.cookiejar_from_dict(cookies_dict, cookiejar=None, overwrite=True)
                break
        return cookies
