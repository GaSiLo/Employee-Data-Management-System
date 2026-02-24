from flask import Flask,render_template,request,redirect,url_for,flash
import sqlite3




app=Flask(__name__)
app.secret_key="supersecretkey"
def get_db_connection():
    conn=sqlite3.connect('Employees.db')
    conn.row_factory=sqlite3.Row
    return conn

@app.route('/')
def index():
    conn=get_db_connection()
    search=request.args.get('search',' ').strip()
    if search:
        query='SELECT * FROM employees WHERE name LIKE ? OR emp_id LIKE ?'
        para=(f'%{search}%', f'%{search}%')
        employees=conn.execute(query,para).fetchall()
    else:
        employees=conn.execute('SELECT * FROM employees order by RANDOM() LIMIT 10').fetchall()
        
        
    conn.close()
    return render_template('index.html',employees=employees)



@app.route('/add',methods=('GET','POST'))
def add_employee():
    if request.method=='POST':
        emp_id = request.form.get('emp_id')
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        gender = request.form.get('gender')
        marital_status = request.form.get('marital_status')
        department = request.form.get('department')
        job_role = request.form.get('job_role')
        salary = request.form.get('salary')
        experience = request.form.get('experience')
        job_level = request.form.get('level')
        
        conn=None
        
        try:

            conn=get_db_connection()
            conn.execute('''
                         INSERT INTO employees (
                    emp_id, name, email, age, gender, marital_status, 
                    department, job_role, salary, experience, job_level
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?)''', 
                (emp_id, name, email, age, gender, marital_status, 
                 department, job_role, salary, experience, job_level)
            )
            conn.commit()
           
            flash(f'Successfully added {name} to the database!','success')
            return redirect(url_for('add_employee'))
        except sqlite3.IntegrityError:
            flash('Error: this id / email already exists in the system.','danger')
        except Exception as e:
            flash(f'An Error has occured: {str(e)}','danger')
        finally:
            if conn:
                conn.close()
    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    conn=None
    try:
        conn = get_db_connection()
        employee = conn.execute('SELECT name FROM employees WHERE emp_id = ?', (id,)).fetchone()

        if employee:
            emp_name = employee['name']
            conn.execute('DELETE FROM employees WHERE emp_id = ?', (id,))
            conn.commit()
            flash(f'Successfully deleted {emp_name}', 'success')
        else:
            flash('Error: Employee record not found.', 'danger')
            
    except Exception as e:
        flash(f'An error occurred during deletion: {str(e)}', 'danger')
    finally:
        if conn:
            conn.close()
            
    return redirect(url_for('index'))

if __name__=='__main__':
    app.run(debug=True)















































































# @app.route('/update/<int:id>',methods=('GET','POST'))
# def update_employee(id):
#     conn=get_db_connection()
#     emp=conn.execute('SELECT * FROM employees where emp_id=?',(id,)).fetchone()
#     if request.method=='POST':
#         name=request.form['name']
#         dept=request.form['dept']
#         conn.execute('UPDTAE employees SET name=?, dept=? WHERE emp_id=?',(name,dept,id))
#         conn.commit()
#         conn.close()
#         redirect(url_for('index'))
#     return render_template('update.html',emplyee=emp)



# app=Flask(__name__)

# logging.basicConfig(filename='master.log',
#                     level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(message)s',
#                     force=True
#                     )
# @app.route('/')
# def index():
#     search=request.args.get('search','')
#     if search :
#         employees=db.seacrh_employees(search)
#     else:
#         employees=db.get_all_employees()    
#         return 

# @app.route('/delete/<int:id>')
# def delete(id):
#     try:
#         db.detele_employee(id)
#         logging.info("Successfully deleted employee ID :{id}")
#     except Exception as e:
#         logging.error(f"Error deleting ID {id}: {e}")
#         return redirect(url_for('index'))

# if __name__=="__main__":
#     app.run(debug=True)