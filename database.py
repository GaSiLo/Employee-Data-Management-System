import sqlite3
import logging 
import os

class DatabaseManager:
    def __init__(self,db_name='Employees.db'):
        self.logger = logging.getLogger(__name__)
        self.db_name=db_name
        #self._setup_logging()

    # def _setup_logging(self):
    #     logging.basicConfig(    
    #     filename='database_errors.log',
    #     level=logging.INFO,
    #     format='%(asctime)s - %(levelname)s - %(message)s',
    #     force=True
    # )

    def get_connection(self):
        try:
            conn=sqlite3.connect(self.db_name)
            conn.row_factory=sqlite3.Row
            return conn
        except sqlite3.Error as e:
            logging.error(f"Error Connecting to database: {e}")
            return None
    
    def init_db(self):
        conn=self.get_connection()
        if conn is None:
            return
        try:
            cursor=conn.cursor()
            cursor.execute('''
                  CREATE TABLE IF NOT EXISTS Employees(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emp_id INTEGER INIQUE NOT NULL,
                    name TEXT NOT NULL,
                    email  TEXT UNIQUE NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    marital_status TEXT,
                    department TEXT,
                    job_role TEXT,
                    salary REAl,
                    experience INTEGER,
                    job_level INTEGER
                )
            ''')
            conn.commit()
            self.logger.info("Table Employees created successfully.")
        except sqlite3.Error as e:
            self.logger.error(f"Failed to create table: {e}")
        finally:
            conn.close()

def get_db_connection():
    # return DatabaseManager.get_connection()
    manager = DatabaseManager()
    return manager.get_connection()
# if __name__=='__main__':
#     manager=DatabaseManager()
#     manager.init_db()