# -*- coding: utf-8 -*-
import json
import requests
from ..log import logger


class DingRobot(object):

    RET_OK = 0

    def __init__(self, web_hook_service_map):
        self.web_hook_service_map = web_hook_service_map

    def emit(self, title, content, service_name=None):

        full_content = '\n\n'.join([title, content])
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({"msgtype": "text", "text": {"content": full_content}})

        res_list = []
        for web_hook, service_list in self.web_hook_service_map.items():
            if service_name in service_list:
                rsp = requests.post(web_hook, data=data, headers=headers).json()
                res_list.append(rsp['errcode'] in [self.RET_OK, ])
        return False not in res_list
