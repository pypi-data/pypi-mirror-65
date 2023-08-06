# -*- coding: utf-8 -*-
import copy
import functools
from redis import StrictRedis

from .log import logger


def check_expire(func):
    """
    自动过期装饰器,给第一个参数name自动设置过期时间,默认是3天
    :param func:
    :return:
    """
    @functools.wraps(func)
    def wrapper_func(self, name, *args, **kwargs):
        ret = func(self, name, *args, **kwargs)

        if self.auto_expire:
            self.set_expire(name)
            # logger.debug('set expire, name: %s, ttl: %s', name, self.rds.ttl(name))

        return ret
    return wrapper_func


class BaseRedis(StrictRedis):
    """
    重写从redis取数据的接口，为了把数据格式转换成unicode
    """

    def get(self, name):
        # type: (object) -> object
        """
        Return the value at key ``name``, or None if the key doesn't exist
        """
        result = super(BaseRedis, self).get(name)
        if not result:
            return result

        if isinstance(result, str):
            try:
                return result.decode('utf-8')
            except Exception as e:
                logger.fatal("decode utf8 error, name: %s, result: %s, e: %s",
                             name, result, e, exc_info=True)

        return result

    def mget(self, keys, *args):
        """
        Returns a list of values ordered identically to ``keys``
        """
        result = super(BaseRedis, self).mget(keys, *args)
        if not result:
            return result

        tmp_result = []

        for item in result:
            if isinstance(item, str):
                try:
                    tmp_result.append(item.decode('utf-8'))
                except Exception as e:
                    tmp_result.append(item)
                    logger.fatal("decode utf8 error, item: %s, result: %s, keys: %s, args: %s, e: %s",
                                 item, result, keys, e, exc_info=True)
            else:
                tmp_result.append(item)

        return tmp_result

    def smembers(self, name):
        "Return all members of the set ``name``"
        result = super(BaseRedis, self).smembers(name)
        if not result:
            return result

        tmp_result = []

        for item in result:
            if isinstance(item, str):
                try:
                    tmp_result.append(item.decode('utf-8'))
                except Exception as e:
                    tmp_result.append(item)
                    logger.fatal("decode utf8 error, item: %s, result: %s, name: %s, args: %s, e: %s",
                                 item, result, name, e, exc_info=True)
            else:
                tmp_result.append(item)

        return tmp_result

    def hget(self, name, key):
        "Return the value of ``key`` within the hash ``name``"
        result = super(BaseRedis, self).hget(name, key)
        if not result:
            return result

        if isinstance(result, str):
            try:
                return result.decode('utf-8')
            except Exception as e:
                logger.fatal("decode utf8 error, name: %s, result: %s, e: %s",
                             name, result, e, exc_info=True)

        return result

    def hgetall(self, name):
        "Return a Python dict of the hash's name/value pairs"
        result = super(BaseRedis, self).hgetall(name)
        if not result:
            return result

        tmp_result = dict()

        for key, value in result.iteritems():
            if isinstance(value, str):
                try:
                    tmp_result[key] = value.decode('utf-8')
                except Exception as e:
                    tmp_result[key] = value
                    logger.fatal("decode utf8 error, key: %s, value: %s, result: %s, name: %s, e: %s",
                                 key, value, result, name, e, exc_info=True)
            else:
                tmp_result[key] = value

        return tmp_result

    def hmget(self, name, keys, *args):
        "Returns a list of values ordered identically to ``keys``"
        result = super(BaseRedis, self).hmget(name, keys, *args)
        if not result:
            return result

        tmp_result = []

        for item in result:
            if isinstance(item, str):
                try:
                    tmp_result.append(item.decode('utf-8'))
                except Exception as e:
                    tmp_result.append(item)
                    logger.fatal("decode utf8 error, item: %s, result: %s, name: %s, args: %s, e: %s",
                                 item, result, name, e, exc_info=True)
            else:
                tmp_result.append(item)

        return tmp_result


class HelperRedis(object):
    # redis原链接对象,如果不希望自动过期，使用该对象来写数据
    rds = None
    # 使用那个库
    db_name = None
    # 保存所有链接,全局化
    connections = dict()
    # 修改数据时是否自动设置过期时间
    auto_expire = False

    # 需要配置文件可配
    # _REDIS_HOST = '127.0.0.1'
    # _REDIS_PASSWORD = 'Qff60f9a1b5470'
    # _REDIS_PORT = 6379
    # _REDIS_DB_SELECT = 2
    # _REDIS_AUTO_EXPIRE = False
    # _REDIS_APP_DEFAULT_EXPIRE_SECONDS = 24 * 60 * 60
    #
    # redis_setting = dict(
    #     host=_REDIS_HOST,
    #     port=_REDIS_PORT,
    #     password=_REDIS_PASSWORD,
    #     db=_REDIS_DB_SELECT,
    #     auto_expire=_REDIS_AUTO_EXPIRE,
    # )

    def __init__(self, db_name, redis_setting):
        _conf = copy.deepcopy(redis_setting)

        self.rds = self.connections.get(db_name)
        if not self.rds:
            self.connections[db_name] = self.rds = BaseRedis(**_conf)

    def set_expire(self, name, expire_time=24*60*60):
        self.rds.expire(name, expire_time)

    @check_expire
    def set(self, *args, **kwargs):
        return self.rds.set(*args, **kwargs)

    @check_expire
    def mset(self, *args, **kwargs):
        return self.rds.mset(*args, **kwargs)

    @check_expire
    def hset(self, *args, **kwargs):
        return self.rds.hset(*args, **kwargs)

    @check_expire
    def hdel(self, *args, **kwargs):
        return self.rds.hdel(*args, **kwargs)

    @check_expire
    def hmset(self, *args, **kwargs):
        return self.rds.hmset(*args, **kwargs)

    @check_expire
    def hget(self, *args, **kwargs):
        return self.rds.hget(*args, **kwargs)

    @check_expire
    def sadd(self, *args, **kwargs):
        return self.rds.sadd(*args, **kwargs)

    @check_expire
    def hscan(self, *args, **kwargs):
        return self.rds.hscan(*args, **kwargs)

    @check_expire
    def hscan_iter(self, *args, **kwargs):
        return self.rds.hscan_iter(*args, **kwargs)

    @check_expire
    def setnx(self, *args, **kwargs):
        return self.rds.setnx(*args, **kwargs)

    def __getattr__(self, item):
        return getattr(self.rds, item)


class FlylogMsgCache(object):

    REDIS_KEY_FLYLOG_MSG = 'redis_key_flylog_msg_{content_md}'

    def __init__(self, content_md, redis_setting):
        self.redis_key = self.REDIS_KEY_FLYLOG_MSG.format(content_md=content_md)

        self.db_name = redis_setting.pop('db_name', 'app_default')
        self.auto_expire_time = redis_setting.pop('auto_expire_time', 24*60*60)
        self.redis_setting = redis_setting

        self.rds = HelperRedis(self.db_name, self.redis_setting)

    def get(self):
        return self.rds.get(self.redis_key)

    def set_times(self):
        if not self.redis_setting:
            return

        count = self.rds.incrby(self.redis_key, 1)
        if count == 1:
            self.rds.set_expire(self.redis_key, self.auto_expire_time)

    def get_times(self):
        times = self.get()
        return int(times) if times else 0
