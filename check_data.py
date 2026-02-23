from database import DatabaseManager  
import logging

class data_view():
    def __init__(self):
        
        self.db_manager = DatabaseManager() 
        self.logger = logging.getLogger(__name__)
    
    def display_records(self, limit=10):
        conn = self.db_manager.get_connection()
        if not conn:
            return
            
        # query = "SELECT * FROM Employees LIMIT ?"
        
        try:
            # cursor = conn.cursor()
            # rows = cursor.execute(query, (limit,)).fetchall()
            rows = conn.execute("SELECT * FROM Employees LIMIT ?", (limit,)).fetchall()
            if not rows:
                print("No records found.") 
                return

            self._print_header()
            for row in rows:
                # self._print_row(row)
                 print(f"{row['emp_id']:<6} | {row['name']:<20} | {row['email']:<30} |"
                       f"{row['age']:<4} | {row['gender']:<6} | {row['marital_status']:<10} |"
                       f"{row['department']:<30} | {row['job_role']:<30} | {row['salary']:<8.0f} |"
                       f"{row['experience']:<4} | {row['level']:<4}")
                
        except Exception as e:
            self.logger.error(f"Database read error: {e}")
        finally:
                conn.close()

    def _print_header(self):
        header = (f"{'Emp_ID':<6} | {'Name':<20} | {'Email':<30} |"
                  f"{'Age': <4} | {'Gen':<6} | {'Status':<10} |"
                  f"{'Dept':<30} | {'Role':<30} | {'Salary':<8} |"
                  f"{'Exp':<4} | {'Lvl':<4}")
        print(header)
        
    
    # def _print_row(self, row):
    
    #     print(f"{row['emp_id']:<10} | {row['name']:<20} | {row['email']:<30} |"
    #           f"{row['age']:<3} | {row['gender']:<6} | {row['marital_status']:<15} |"
    #           f"{row['department']:<20} | {row['job_role']:<20} | {row['salary']:<8.0f} |"
    #           f"{row['experience']:<4} | {row['level']:<4}")

# if __name__ == '__main__':  
#     view_data = data_view()
#     view_data.display_records(limit=10)