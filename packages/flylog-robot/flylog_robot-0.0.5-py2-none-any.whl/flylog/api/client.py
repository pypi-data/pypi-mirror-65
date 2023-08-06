# -*- coding: utf-8 -*-

import socket
import json
from .. import constants


class Client(object):

    sock = None

    def __init__(self, host=None, port=None):
        self.host = host or constants.HOST
        self.port = port or constants.PORT

        # 一开始就创建好sock
        self._create_socket()

    def send(self, source, content, role_list=None):
        """
        发送
        """
        s = json.dumps(dict(source=source, role_list=role_list, content=content))
        # python3的json.dumps返回的是str
        if not isinstance(s, bytes):
            s = s.encode('utf-8')
        self.sock.sendto(s, (self.host, self.port))

    def _create_socket(self):
        """
        创建socket
        """
        # 先尝试关闭掉
        self.close()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def close(self):
        """
        关闭
        """
        if self.sock is None:
            return

        try:
            self.sock.close()
        except:
            pass
        finally:
            self.sock = None
