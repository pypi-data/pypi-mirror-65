import sys
import time

import redis
from redis.client import Pipeline, Redis

from re_common.baselibrary import IniConfig


class MyRedis(object):
    def __init__(self, configpath=""):
        self.configpath = configpath

    def set_configpath(self, configpath):
        self.configpath = configpath

    def set_redis_from_config(self, sesc="proxy", encoding="utf-8"):
        assert self.configpath != "", 'configpath 为空，请调用set_configpath'
        dictsall = IniConfig(self.configpath).get_conf_dict(encoding=encoding)
        dicts = dictsall[sesc]
        self.RedisHost = dicts['RedisHost']
        self.RedisPort = dicts['RedisPort']
        self.RedisDB = dicts['RedisDB']
        self.RedisKey = dicts['RedisKey']

    def conn_redis(self):
        assert self.RedisHost, 'RedisHost 不存在，请先调用set_redis_from_config'
        assert self.RedisPort, 'RedisPort 不存在，请先调用set_redis_from_config'
        assert self.RedisDB, 'RedisDB 不存在，请先调用set_redis_from_config'
        assert self.RedisKey, 'RedisKey 不存在，请先调用set_redis_from_config'
        self.rconn = redis.StrictRedis(host=self.RedisHost, port=self.RedisPort, db=self.RedisDB, decode_responses=True)
        return self.rconn

    def getDataFromRedis(self):
        assert self.RedisKey, 'RedisKey 不存在，请先调用set_redis_from_config'
        assert self.rconn, 'rconn 不存在，请先调用conn_redis'
        if self.rconn:
            rows = self.rconn.smembers(self.RedisKey)
            return rows
        else:
            print("redis出现连接错误")
            sys.exit(-1)

    def get_pipeline(self):
        assert isinstance(self.rconn, Redis), Exception("请调用conn_redis获取")
        self.pipe = self.rconn.pipeline()
        return self.pipe

    def delete(self, RedisKey):
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.delete(RedisKey)

    def sadd(self, name, ProxyPoolValid: set):
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.sadd(name, *ProxyPoolValid)
        self.pipe.execute()

    def hset(self, name, key, value):
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.hset(name, key, value)
        self.pipe.execute()

    def hget(self, name, key):
        assert isinstance(self.pipe, Pipeline), Exception("请调用get_pipeline获取")
        self.pipe.hget(name, key)
        self.pipe.execute()

    def set(self, name, value):
        self.rconn.set(name, value)

    def get(self, name):
        return self.rconn.get(name)


def RedisConnect(configpath, sesc="proxy", encoding="utf-8"):
    """
    连接数据库 通过读取配置文件连接,如果读取配置文件 失败  返回None
    :return:
    """
    dictsall = IniConfig(configpath).get_conf_dict(encoding=encoding)
    dicts = dictsall[sesc]
    RedisHost = dicts['RedisHost']
    RedisPort = dicts['RedisPort']
    RedisDB = dicts['RedisDB']
    RedisKey = dicts['RedisKey']
    try:
        rconn = redis.StrictRedis(host=RedisHost, port=RedisPort, db=RedisDB, decode_responses=True)
    except:
        # 有可能因为网络波动无法连接 这里休眠10秒重连一次  如果还是失败就放弃
        time.sleep(10)
        rconn = redis.StrictRedis(host=RedisHost, port=RedisPort, db=RedisDB, decode_responses=True)
    if rconn:
        return rconn, RedisKey
    return None


def getDataFromRedis(configpath, sesc="proxy"):
    rconn, RedisKey = RedisConnect(configpath, sesc=sesc)
    if rconn:
        rows = rconn.smembers(RedisKey)
        return rows
    else:
        print("redis出现连接错误")
        sys.exit(-1)
