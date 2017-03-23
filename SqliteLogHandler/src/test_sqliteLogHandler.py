from AppLoggerMaker import AppLoggerMaker

def getLogger():
    logmaker = AppLoggerMaker()
    logger = logmaker \
        .append_default_handler() \
        .append_sqlite_handler() \
        .get_app_logger()
    return logger


logger = getLogger()
logger.debug('hello world!!')
logger.info('hello world!!')
    