import logging

from re_common.baselibrary.utils.basedir import BaseDir
from re_common.baselibrary import BaseFile
from re_common.baselibrary import MLogger


def test_mlogger_streamlogger():
    """
    只打印数据不计入文件
    pytest mylogger_test.py::test_mlogger_streamlogger -s
    :return:
    """
    streamlogger = MLogger().streamlogger
    streamlogger.setLevel(logging.DEBUG)
    streamlogger.info("mesg info")
    streamlogger.warning("msg warning")
    streamlogger.warn("msg warn")
    streamlogger.error("msg error")
    streamlogger.debug("msg debug")
    streamlogger.critical("msg critical")
    streamlogger.exception("msg exception")


def test_mlogger_filelogger():
    """
    测试将日志写入文件中　文件名以日期自动生成　如20200211.log
    pytest mylogger_test.py::test_mlogger_filelogger -s
    文件流的logger
    :param filedir:
    :return:
    """
    filedir = BaseDir.get_file_dir_absolute(__file__)
    filelogger = MLogger(filedir).filelogger
    filelogger.setLevel(logging.DEBUG)
    filelogger.info("mesg info")
    filelogger.warning("msg warning")
    filelogger.warn("msg warn")
    filelogger.error("msg error")
    filelogger.debug("msg debug")
    filelogger.critical("msg critical")
    filelogger.exception("msg exception")


def test_mlogger_allloger():
    """
    测试将日志写入文件中 有一个以日期的总文件　以及每个级别的分文件
    pytest mylogger_test.py::test_mlogger_allloger -s
    文件流的logger
    :param filedir:
    :return:
    """
    filedir = BaseDir.get_file_dir_absolute(__file__)
    filedir = BaseFile.get_new_path(filedir, "log")
    BaseDir.create_dir(filedir)
    filelogger = MLogger(filedir).alllogger
    filelogger.setLevel(logging.DEBUG)
    filelogger.info("mesg info")
    filelogger.warning("msg warning")
    filelogger.warn("msg warn")
    filelogger.error("msg error")
    filelogger.debug("msg debug")
    filelogger.critical("msg critical")
    filelogger.exception("msg exception")
