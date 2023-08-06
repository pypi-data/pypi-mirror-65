class BaseAbs(object):
    @staticmethod
    def get_sql_factory():
        from .database.sql_factory import SqlFactory
        return SqlFactory()

    @staticmethod
    def get_config_factory():
        from .readconfig.config_factory import ConfigFactory
        return ConfigFactory()



