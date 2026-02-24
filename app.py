from flask import Flask,render_template,request,redirect,url_for
import sqlite3




app=Flask(__name__)
def get_db_connection():
    conn=sqlite3.connect('Employees.db')
    conn.row_factory=sqlite3.Row
    return conn

@app.route('/')
def index():
    conn=get_db_connection()
    search=request.args.get('search')
    if search:
        query='SELECT * FROM employees WHERE name LIKE ? OR department LIKE ?'
        para=('%' + search + '%', '%' + search + '%')
        employees=conn.execute(query,para).fetchall()
    else:
        employees=conn.execute('SELECT * FROM employees').fetchall()
        
        
    conn.close()
    return render_template('index.html',employees=employees)



@app.route('/add',methods=('GET','POST'))
def add_employee():
    if request.method=='POST':
        emp_id=request.form['emp_id']
        name=request.form['name']
        email=request.form['email']
        age=request.form['age']
        gender=request.form['gender']
        marital_status=request.form['marital_status']
        department=request.form['department']
        job_role=request.form['job_role']
        salary=request.form['salary']
        experience=request.form['experience']
        job_level= request.form['job_level']
        conn=get_db_connection()
        conn.execute('INSERT INTO employees (emp_id,name,email,age,gender,marital_status,department,job_role,salary,experience,job_level) values(?,?,?,?,?,?,?,?,?,?,?)',(emp_id,name,email,age,gender,marital_status,department,job_role,salary,experience,job_level)
                     )

        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add.html')


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