import logging

from .base import BaseStorage


class LogEngine(BaseStorage):
    def __init__(self, config=None):
        super(LogEngine, self).__init__(),
        self.config = config
        self.logger_name = self.config.get("LOGGER_NAME", "root")
        self.logger = logging.getLogger(self.logger_name)

    def filter(self, criteria):
        pass

    def getSummary(self, criteria):
        pass

    def insert(self, measurement):
        self.logger.info("{}".format(measurement))
        return True

    def delete(self, measurementId):
        pass

    def truncate(self):
        pass
