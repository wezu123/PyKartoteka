import logging

class Log:
    def __init__(self, severity=logging.DEBUG):
        logging.basicConfig(
            level=severity,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            filename='debug.log'
        )

        # self.path = 'runtime.log'
        # self.severity = severity

        # self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # self.file_handler = logging.FileHandler(self.path)
        # self.file_handler.setLevel(severity)
        # self.file_handler.setFormatter(self.formatter)

        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(logging.ERROR)
        # self.logger.addHandler(self.file_handler)