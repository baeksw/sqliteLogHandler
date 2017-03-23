'''
Created on 2017. 3. 23.

@author: BaekSeungWoo
'''
import os
import sqlite3
import threading
import logging
from datetime import datetime

CREATE_APPLITION_TABLE = '''CREATE TABLE "{}" (
    id INTEGER NOT NULL, 
    name VARCHAR(1000), 
    process INTEGER NOT NULL, 
    "processName" VARCHAR(1000), 
    "threadName" VARCHAR(1000), 
    filename VARCHAR(1000), 
    pathname VARCHAR(1000), 
    levelname VARCHAR(100), 
    lineno INTEGER, 
    asctime VARCHAR(100), 
    msg TEXT, 
    message TEXT, 
    module VARCHAR(500), 
    levelno INTEGER, 
    PRIMARY KEY (id)
)
'''

EXIST_TABLE_QUERY = '''
SELECT name FROM sqlite_master WHERE name='{}' COLLATE NOCASE
'''

INSERT_APP_LOG = '''INSERT INTO {tableName} (
      name
    , process
    , processName
    , threadName
    , filename
    , pathname
    , levelname
    , lineno
    , asctime
    , msg
    , message
    , module
    , levelno
    ) VALUES (
      '{name}'
    , '{process}'
    , '{processName}'
    , '{threadName}'
    , '{filename}'
    , '{pathname}'
    , '{levelname}'
    ,  {lineno}
    , '{asctime}'
    , '{msg}'
    , '{message}'
    , '{module}'
    ,  {levelno}
    )
'''

class SQLiteLogHandler(logging.Handler):
    def __init__(self, db='sqlite_log', level=logging.NOTSET,sema_value=1):
        self.semaphore = threading.BoundedSemaphore(sema_value)
        logging.Handler.__init__(self, level)
        self.db = db

    def emit(self, record):
        data = record.__dict__.copy()
        table_name = self.get_table_name()
        
        # LOCK ACCQUIRE
        self.semaphore.acquire()
        if self.exist_table(table_name) == False:
            self.table_name = self.create_application_log_table()
        self.semaphore.release()
        # LOCK RELEASE

        data['tableName'] = table_name
        query = INSERT_APP_LOG.format(**data)
                    
        try:
            self.commit_data(query)
        except Exception as e:
            pass

    def commit_data(self,query):
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        try:
            cur.execute(query)
            con.commit()
        except Exception as e:
            pass
        finally:
            con.close()

    def create_application_log_table(self):
        DML = CREATE_APPLITION_TABLE.format(self.get_table_name())
        con = sqlite3.connect(self.db)
        cursor = con.cursor()
        try:
            cursor.execute(DML)
            con.commit()
        except Exception as e:
            pass
        finally:
            con.close()

    def exist_table(self,table_name):
        con = sqlite3.connect(self.db)
        query = EXIST_TABLE_QUERY.format(table_name)
        c = con.cursor()
        c.execute(query,())
        buf = [ x for x in c.fetchall() ]
        con.close()
        return False if len(buf) == 0 else True
    
    def get_table_name(self):
        month = datetime.now().strftime('%Y%m')
        tableName = 'APPLICATION_LOG_'+month
        return tableName

        