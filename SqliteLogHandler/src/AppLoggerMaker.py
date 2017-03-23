import os
import logging
from logging.handlers import RotatingFileHandler
from SQLiteLogHandler import SQLiteLogHandler

class AppLoggerMaker(object):
    def __init__(self,logger_name='AppLogger'):
        self.fomatter = logging.Formatter('[ %(levelname)s ][ %(filename)s:%(lineno)s - %(asctime)s ] - %(message)s')
        logging.basicConfig(level=logging.DEBUG)
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.handler = []
        
    def append_default_handler(self):
        if 'DEFAULT' not in self.handler:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(self.fomatter)
            self.logger.addHandler(streamHandler)
            self.handler.append('DEFAULT')
        return self
    
    def append_file_handler(self):
        if 'FILE' not in self.handler:
            log_file = './{}.log'.format(self.logger_name)
            fileMaxByte = 1024 * 1024 * 100 #100MB
            fileHandler = RotatingFileHandler(log_file,maxBytes=fileMaxByte,backupCount=100)
            fileHandler.setFormatter(self.fomatter)
            self.logger.addHandler(fileHandler)
            self.handler.append('FILE')
        return self
    
    def append_sqlite_handler(self,sema_value=1):
        if 'SQLITE' not in self.handler:
            db='{}.db'.format(self.logger_name)
            sqliteHandler = SQLiteLogHandler(db=db,sema_value=sema_value)
            sqliteHandler.setFormatter(self.fomatter)
            self.logger.addHandler(sqliteHandler)
            self.handler.append('SQLITE')
        return self
    
    def get_app_logger(self):
        self.append_default_handler()
        return self.logger
