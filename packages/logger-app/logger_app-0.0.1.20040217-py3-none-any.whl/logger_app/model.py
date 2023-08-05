# -*- coding: utf-8 -*- 
# @Time     : 2020-02-06 15:34
# @Author   : binger
import json
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
from funcy import project


class JsonStyle(object):
    """自定义 json 格式数去规则 """
    TO_STR = lambda info: json.dumps(info, separators=(",", ":"), ensure_ascii=False)
    default_format = ('message',)
    asctime_format = 'asctime'
    asctime_search = 'asctime'

    def __init__(self, fmt):
        self._fmt = fmt or self.default_format

    def usesTime(self):
        return self.asctime_search in self._fmt

    def format(self, record):
        keys = set(filter(lambda key: getattr(record, key, False), ["exc_text", "stack_info"]))
        if keys:
            keys.update(self._fmt)
        else:
            keys = self._fmt
        a = project(record.__dict__, keys)
        s = JsonStyle.TO_STR(a)
        return s


# 添加 json 日志格式
logging._STYLES["json"] = (JsonStyle, '{"levelname": levelname, "message":message}')


class FormatterRule(logging.Formatter):  # 自定义格式化类
    """重新实现日志输出规则工厂"""
    CB_TAG_MAP = {}

    def __init__(self, fmt=None, datefmt=None, style='%', cb_tag_map=None):
        self._cb_tag_map = cb_tag_map or self.CB_TAG_MAP
        if style != "json":
            field = ' '.join(list(map(lambda s: '%({})-2s'.format(s), self._cb_tag_map.keys())))
            fmt = fmt or '%(asctime)s.%(msecs)03d:{} %(filename)-12s[%(lineno)4d] %(levelname)-6s %(message)s'.format(
                field)
        else:
            fmt = {"asctime", "msecs", "filename", "lineno", "levelname", "message"}
            fmt.update(self._cb_tag_map.keys())
        # datefmt = '%Y-%m-%d %H:%M:%S'
        self.__fmt_style = style
        super(FormatterRule, self).__init__(fmt, datefmt, style)

    def format(self, record):
        """每次生成日志时都会调用, 该方法主要用于设置自定义的日志信息
        :param record 日志信息"""
        for tag, cb in self._cb_tag_map.items():
            setattr(record, tag, cb())

        if self.__fmt_style != "json":
            return super().format(record)  # 执行父类的默认操作
        else:
            record.message = record.getMessage()
            if self.usesTime():
                record.asctime = self.formatTime(record, self.datefmt)

            if record.exc_info:
                # Cache the traceback text to avoid converting it multiple times
                # (it's constant anyway)
                if not record.exc_text:
                    record.exc_text = self.formatException(record.exc_info)
            if record.stack_info:
                record.stack_info = self.formatStack(record.stack_info)

            return self.formatMessage(record)


def register_formatter_tag_mapper(mapper):
    """注册日志输出格式标识"""
    FormatterRule.CB_TAG_MAP = mapper


def load_styles():
    """获取日志风格"""
    return list(logging._STYLES.keys())


class LoggerApp(object):
    def __init__(self, name, level="INFO", enable_console=True, fmt=None):
        self.name = name
        self._enable_console = enable_console
        self._default_global_level = "DEBUG"
        self._console_fmt = '%(asctime)s.%(msecs)03d:%(filename)-12s[%(lineno)4d] %(levelname)-6s %(message)s'
        self.default_level = level
        self.fmt = fmt

        self._logger = logging.getLogger(self.name)

    @property
    def logger(self):
        return self._logger

    @property
    def enable_console(self):
        return self._enable_console

    @enable_console.setter
    def enable_console(self, v):
        self._enable_console = v

    def rotating_by_size(self, filename=None, maxBytes=None, backupCount=10):
        """

        :param filename:
        :param maxBytes: 单位为 B，1M = 1 * 1024 * 1024
        :param backupCount: 日志文件个数
        :return:
        """
        file_handler = RotatingFileHandler(filename=filename or "{}.log".format(self.name),
                                           maxBytes=maxBytes or 100 * 1024 * 1024,
                                           backupCount=backupCount,
                                           encoding=None, delay=False)  # 转存文件处理器  当达到限定的文件大小时, 可以将日志转存到其他文件中

        return self._create_logger(file_handler, self.fmt)

    def rotating_by_time(self, filename=None, when='d', interval=1, backupCount=0, encoding=None, delay=False,
                         utc=False,
                         atTime=None):
        """
        按时间形式回滚日志文件
        :param filename:
        :param when: 回滚周期的单位
        :param interval: 几个回滚周期的单位。即：when * interval 为回滚周期
        :param backupCount: 保留的日志文件个数
        :param encoding:
        :param delay:
        :param utc:
        :param atTime:
        :return:
        """
        file_handler = TimedRotatingFileHandler(filename=filename or "{}.log".format(self.name),
                                                when=when, interval=interval,
                                                backupCount=backupCount,
                                                encoding=encoding,
                                                delay=delay,
                                                atTime=atTime,
                                                utc=utc)
        return self._create_logger(file_handler, self.fmt)

    def create_logger(self, is_time_rotating=False):
        if is_time_rotating:
            return self.rotating_by_time()
        else:
            return self.rotating_by_size()

    def _create_logger(self, file_handler, fmt=None):
        """配置 日志"""
        # 创建flask.app日志器
        flask_logger = self.logger
        # 设置全局级别
        flask_logger.setLevel(self._default_global_level)

        if self._enable_console:
            # 创建控制台处理器
            console_handler = logging.StreamHandler()

            # 给处理器设置输出格式
            console_formatter = logging.Formatter(fmt=self._console_fmt)
            console_handler.setFormatter(console_formatter)

            # 日志器添加处理器
            flask_logger.addHandler(console_handler)

        # # 创建文件处理器
        # file_handler = RotatingFileHandler(filename='flask.log', maxBytes=100 * 1024 * 1024,
        #                                    backupCount=10)  # 转存文件处理器  当达到限定的文件大小时, 可以将日志转存到其他文件中

        # 给处理器设置输出格式
        file_formatter = fmt or FormatterRule()
        file_handler.setFormatter(fmt=file_formatter)
        # 单独设置文件处理器的日志级别
        file_handler.setLevel(self.default_level)

        # 日志器添加处理器
        flask_logger.addHandler(file_handler)
        return flask_logger
