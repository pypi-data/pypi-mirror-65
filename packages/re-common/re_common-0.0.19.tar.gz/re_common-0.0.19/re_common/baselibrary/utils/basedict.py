class BaseDicts(object):

    @classmethod
    def removeDictsNone(self, dicts: dict) -> dict:
        """
        去除字典中值为None的键值
        :param dicts:
        :return:
        """
        return {key: value for key, value in dicts.items() if value is not None}

    @classmethod
    def removeDictsStringNull(self, dicts: dict) -> dict:
        """
        去除字典中值为''的键值
        :param dicts:
        :return:
        """
        return {key: value for key, value in dicts.items() if value == ""}

    @classmethod
    def removeDictsAllNone(self, dicts: dict) -> dict:
        """
        去除字典中值为'' 和 None 的键值
        :param dicts:
        :return:
        """
        return {key: value for key, value in dicts.items() if value == "" or value is not None}

    @classmethod
    def sortkeys(self, dicts, reverse=False):
        """
        默认升序排序，加  reverse = True 指定为降序排序
        通过keys 对dicts 排序
        经过测试是新的列表
        :return:
        """
        return {k: dicts[k] for k in sorted(dicts.keys(), reverse=reverse)}

    @classmethod
    def sortvalues(self, dicts, reverse=False):
        """
        默认升序排序，加  reverse = True 指定为降序排序
        d[1] 为值　ｄ[0]　为键
        d 为元组　为dicts的键值
        通过　values 对dicts 排序
        :param dicts:
        :return:
        """
        return {k: v for k, v in sorted(dicts.items(), key=lambda d: d[1], reverse=reverse)}

    @classmethod
    def is_key_have(cls, dicts, key):
        """
        判断key 是否存在,但只能判断一个层次
        :param dicts:
        :param key:
        :return:
        """
        if key in dicts.keys():
            return True
        else:
            return False

    @classmethod
    def is_more_key_have(cls, dicts, keys=[]):
        """
        判断多个key 是否存在　可以有更深的层次
        :param dicts:
        :param keys: ["a.b","c.d"]
        :return:
        """
        for item in keys:
            if item.find("."):
                allstrings = ""
                for key in item.split("."):
                    allstrings = allstrings + '["{}"]'.format(key)
                try:
                    eval("dicts" + allstrings)
                except:
                    return False
            else:
                if item not in dicts.keys():
                    return False
        return True
