import json

import requests


class LoginSpider:
    def __init__(self, cookies):
        self.cookies = cookies
        self.task = None

    def start_task(self):
        config_file = open("../data/config/task_config.json", 'r')
        config_json = json.load(config_file)
        self.task = requests.session()
        self.task.headers = {
            "Accept": config_json["Accept"],
            "Accept-Language": config_json["Accept-Language"],
            "Upgrade-Insecure-Requests": config_json["Upgrade-Insecure-Requests"],
            "User-Agent": config_json["User-Agent"],
            "Accept-Encoding": config_json["Accept-Encoding"],
            "Host": config_json["Host"],
            # "Cookie": self.cookies,
            "Connection": config_json["Connection"]
        }
        self.task.cookies = self.cookies

    def terminate_task(self):
        self.task.close()

    def update_header(self, key, value):
        """
        向headers中添加或修改属性，本场景下是Refer字段
        :param key:header属性名
        :param value:header属性值
        :return:null
        """
        self.task.headers[key] = value
