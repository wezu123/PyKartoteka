import logging

class Log:
    # def __init__(self, severity=logging.DEBUG):
    #     logging.basicConfig(
    #         level=severity,
    #         format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    #         filename='debug.log'
    #     )

    def setup_logger(severity=logging.DEBUG):
        log_file = 'debug.log'
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(severity)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(severity)
        console_handler.setFormatter(formatter)

        logging.basicConfig(
            level=severity,
            handlers=[file_handler, console_handler]
        )