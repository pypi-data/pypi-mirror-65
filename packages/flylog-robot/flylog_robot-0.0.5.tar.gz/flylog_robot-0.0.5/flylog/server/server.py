#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
用来作为接受log传递的agent
通过udp通道。

不使用 gevent，因为测试了 gevent 对 smtplib 似乎没法异步，还是会阻塞
"""

from __future__ import unicode_literals
import time
import datetime


import logging.config
import json
from collections import defaultdict

from .six import socketserver, _thread
from .utils import import_string
from .log import logger
from .redis_helper import FlylogMsgCache
from .utils import TextHandlerPokio


class Server(object):
    backend_dict = None
    LOG_URL = '\nhttps://gm.pokio.com/error_list?md5={md5}&date={date}'

    def __init__(self, config=None):
        self.config = config
        if hasattr(config, 'LOGGING'):
            logging.config.dictConfig(config.LOGGING)

        self.backend_dict = dict()
        for name, backend_conf in self.config.BACKENDS.items():
            _class = import_string(backend_conf['class'])
            backend = _class(**backend_conf['init_data'])

            self.backend_dict[name] = backend

        self.resend_times = config.FILTER_SETTING.get('resend_times', 0)
        self.redis_setting = config.FILTER_SETTING.get('redis_setting', {})

    def filter_backends(self, backends, service_name):
        """
        ding 和 ding robot 的输出互斥，优化输出ding robot
        :param backends:
        :param service_name
        :return:
        """
        robot_config = self.config.BACKENDS.get('robot', None)
        if not robot_config:
            return

        init_data = robot_config.get('init_data', None)
        if not init_data:
            return

        web_hook_service_map = init_data.get('web_hook_service_map', None)
        if not web_hook_service_map:
            return

        robot_service_list = []
        for web_hook, service_list in web_hook_service_map.items():
            robot_service_list += service_list

        logger.info('trace data source: %s, robot_service_list: %s', service_name, robot_service_list)
        if service_name in robot_service_list:
            if backends.get('ding', None):
                backends.pop('ding')
        return

    def _is_reached_message_send_limit(self, content_md):
        return FlylogMsgCache(content_md, self.redis_setting).get_times() >= self.resend_times

    def handle_message(self, message, address):
        recv_dict = json.loads(message)

        source = recv_dict.get('source')
        service_name = recv_dict.get('service_name')
        title = '[%s]Attention!' % source
        content = recv_dict.get('content')

        logger.info('%s\n%s', title, content)

        role_list = recv_dict.get('role_list') or ('default',)

        # backend_name -> params
        merged_backends = defaultdict(dict)

        content_md = ''
        if self.redis_setting:
            content_md = TextHandlerPokio.handle(content)
            if not content_md:
                logger.error('file info invalid content info: %s', content)
                return

            if self._is_reached_message_send_limit(content_md):
                logger.error('log info reached resend limit content: %s', content)
                return

            FlylogMsgCache(content_md, self.redis_setting).set_times()

        for role in role_list:
            handler_list = self.config.ROLES.get(role)
            if handler_list is None:
                continue

            for handler in handler_list:
                backend_name = handler['backend']
                params = handler['params']
                merged_backends[backend_name] = self._merge_backend_params(
                    merged_backends[backend_name],
                    params
                )

        date_time = datetime.datetime.fromtimestamp(int(time.time()))
        date = date_time.strftime('%Y%m%d')
        log_end_url = self.LOG_URL.format(md5=content_md, date=date)
        content += log_end_url

        self.filter_backends(merged_backends, service_name)

        for backend_name, params in merged_backends.items():
            params['service_name'] = service_name
            _thread.start_new_thread(self._process_backend_emit, (backend_name, params, title, content))

    def _merge_backend_params(self, params1, params2):
        """
        因为有可能不同role之间对应同样的发送人，为了避免重复，所以需要合并
        """

        merged_keys = set(params1.keys()) | set(params2.keys())
        merged_params = dict()

        for key in merged_keys:
            value1 = params1.get(key) or list()
            value2 = params2.get(key) or list()

            merged_params[key] = list(set(value1) | set(value2))

        return merged_params

    def _process_backend_emit(self, backend_name, params, title, content):
        """
        为了支持单独线程，所以独立出来
        """
        backend = self.backend_dict[backend_name]

        try:
            if not backend.emit(title, content, **params):
                logger.error('emit error. backend: %s, params: %s, title: %s, content: %s',
                             backend_name, params, title, content)
        except:
            logger.error('exc occur. backend: %s, params: %s, title: %s, content: %s',
                         backend_name, params, title, content, exc_info=True)

    def run(self, host, port):
        class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
            def handle(sub_self):
                message = sub_self.request[0]
                try:
                    self.handle_message(message, sub_self.client_address)
                except:
                    logger.error('exc occur. message: %r, address: %s', message, sub_self.client_address, exc_info=True)

        class MyUDPServer(socketserver.ThreadingUDPServer):
            daemon_threads = True
            allow_reuse_address = True

        logger.info('running on %s:%s', host, port)

        server = MyUDPServer((host, port), ThreadedUDPRequestHandler)

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass
        except:
            logger.error('exc occur.', exc_info=True)
