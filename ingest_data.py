import os
import pandas as pd
import logging
from database import get_db_connection


class DataIngest:
    def __init__(self,folder_name='data',file_name='hr_analytics.csv'):
        self.csv_path=os.path.join(folder_name,file_name)
        self.logger=logging.getLogger(__name__)
    
    # def _setup_logging(self):
    #     logging.basicConfig(
    #     filename='ingestion_errors.log',
    #     level=logging.INFO,
    #     format='%(asctime)s - %(levelname)s - %(message)s',
    #     force=True
    # )
    #     return logging.getLogger(__name__)
    
    def transform_data(self,df):
        self.logger.info("Transforming Data.")
        df_transformed=pd.DataFrame()

        df_transformed['emp_id'] = df['EmployeeNumber'].fillna(0).astype(int)
        df_transformed['name'] = df['Name'].fillna('Unknown')
        df_transformed['email'] = df['Email'].fillna('N/A')
        df_transformed['age'] = pd.to_numeric(df['Age']).fillna(0).astype(int)
        df_transformed['gender'] = df['Gender']
        df_transformed['marital_status'] = df['MaritalStatus']
        df_transformed['department'] = df['Department']
        df_transformed['job_role'] = df['JobRole']
        df_transformed['salary'] = pd.to_numeric(df['MonthlyIncome']).fillna(0.0)
        df_transformed['experience'] = pd.to_numeric(df['TotalWorkingYears']).fillna(0).astype(int)
        df_transformed['level'] = pd.to_numeric(df['JobLevel']).fillna(0).astype(int)
    
        return df_transformed

    def run_ingestion(self):
        conn=None

        try:
            if not os.path.exists(self.csv_path):
                raise FileNotFoundError(f"Missing File:{self.csv_path}")
            
            df_raw=pd.read_csv(self.csv_path)
            # self.logger.info(f"Loaded {len(df_raw)} records.")
        
            df_final=self.transform_data(df_raw)

            conn=get_db_connection()
            df_final.to_sql('Employees',conn, if_exists='replace', index=False)
            conn.commit()

            self.logger.info(f'Successfully ingested {len(df_final)} records.')
        
        except FileNotFoundError as e:
            error_msg=f"File not Found: {e}"
            self.logger.error(error_msg)

        except Exception as e:
            error_msg=f"An unexpected error occurred: {e}"
            self.logger.error(error_msg)      
        finally:
            if conn:
                conn.close()
                # self.logger.info("Database Connection Closed.")
         
# if __name__=='__main__':
#     ingest=DataIngest()
#     ingest.run_ingestion()
   

