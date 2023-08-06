import tempfile
import os
import logging

from . import handlers


class Logger:
    def __init__(
        self,
        logger_name,
        log_level=logging.ERROR,
        log_to_stdout=True,
    ):
        self.logger_name = logger_name
        self.log_level = log_level
        self.log_to_stdout = log_to_stdout

        logs_dir_path = os.path.join(
            tempfile.gettempdir(),
            'sergeant',
            logger_name,
        )
        os.makedirs(
            name=logs_dir_path,
            exist_ok=True,
        )

        self.logger = logging.getLogger(
            name=self.logger_name,
        )
        self.logger.propagate = False

        if log_to_stdout:
            formatter = logging.Formatter(
                fmt='%(asctime)s %(name)-12s %(process)d %(levelname)-8s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
            )
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            self.logger.addHandler(stream_handler)

        self.logger.setLevel(self.log_level)

    def add_logstash_handler(
        self,
        host,
        port,
    ):
        handler = handlers.logstash.LogstashHandler(
            host=host,
            port=port,
        )
        self.logger.addHandler(
            hdlr=handler,
        )

    def debug(
        self,
        msg,
        extra=None,
    ):
        self.logger.debug(
            msg=msg,
            extra=extra,
        )

    def warning(
        self,
        msg,
        extra=None,
    ):
        self.logger.warning(
            msg=msg,
            extra=extra,
        )

    def info(
        self,
        msg,
        extra=None,
    ):
        self.logger.info(
            msg=msg,
            extra=extra,
        )

    def error(
        self,
        msg,
        extra=None,
    ):
        self.logger.error(
            msg=msg,
            extra=extra,
        )

    def critical(
        self,
        msg,
        extra=None,
    ):
        self.logger.critical(
            msg=msg,
            extra=extra,
        )
