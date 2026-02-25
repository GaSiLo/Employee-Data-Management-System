from flask import Flask, render_template, request, redirect, url_for, flash, Response
import sqlite3
import csv
import io
import logging

logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.secret_key = "supersecretkey"

class EmployeeDB:
    def __init__(self, db_path):
        self.db_path = db_path

    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def search(self, term):
        conn = self.get_connection()
        query = 'SELECT * FROM employees WHERE name LIKE ? OR emp_id LIKE ?'
        para = (f'%{term}%', f'%{term}%')
        rows = conn.execute(query, para).fetchall()
        conn.close()
        return rows

    def get_all(self):
        conn = self.get_connection()
        rows = conn.execute('SELECT * FROM employees').fetchall()
        conn.close()
        return rows

    def get_one(self, emp_id):
        conn = self.get_connection()
        row = conn.execute('SELECT * FROM employees WHERE emp_id = ?', (emp_id,)).fetchone()
        conn.close()
        return row

    def add(self, data):
        conn = self.get_connection()
        conn.execute('''INSERT INTO employees (emp_id, name, email, age, gender, marital_status, 
                        department, job_role, salary, experience, job_level) 
                        VALUES (?,?,?,?,?,?,?,?,?,?,?)''', data)
        conn.commit()
        conn.close()

    def update(self, data):
        conn = self.get_connection()
        conn.execute('''UPDATE employees SET name=?, email=?, age=?, gender=?, marital_status=?,
                        department=?, job_role=?, salary=?, experience=?, job_level=?
                        WHERE emp_id=?''', data)
        conn.commit()
        conn.close()

    def delete(self, emp_id):
        conn = self.get_connection()
        conn.execute('DELETE FROM employees WHERE emp_id = ?', (emp_id,))
        conn.commit()
        conn.close()

db = EmployeeDB('Employees.db')

def validate_form(data):
    if not data.get('name') or not data.get('email'):
        return "Name and Email are required."
    try:
        age = int(data.get('age', 0))
        if age < 18:
            return "Age must be 18 or older."
    except ValueError:
        return "Age must be a number."
    return None

@app.route('/')
def index():
    search = request.args.get('search', '').strip()
    employees = db.search(search) if search else []
    return render_template('index.html', employees=employees)

@app.route('/add', methods=('GET', 'POST'))
def add_employee():
    if request.method == 'POST':
        err = validate_form(request.form)
        if err:
            flash(err, 'danger')
            return redirect(url_for('add_employee'))

        data = (
            request.form.get('emp_id'), request.form.get('name'), request.form.get('email'),
            request.form.get('age'), request.form.get('gender'), request.form.get('marital_status'),
            request.form.get('department'), request.form.get('job_role'), request.form.get('salary'),
            request.form.get('experience'), request.form.get('job_level')
        )
        try:
            db.add(data)
            logging.info(f"Successfully ingested 1 record (ID: {data[0]}).")
            flash(f"Successfully added {data[1]}", 'success')
            return redirect(url_for('add_employee'))
        except Exception as e:
            logging.error(f"Add Error: {e}")
            flash(f"Error: {e}", 'danger')
    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    try:
        db.delete(id)
        logging.info(f"Successfully deleted record ID: {id}.")
        flash("Successfully deleted record", 'success')
    except Exception as e:
        logging.error(f"Delete Error: {e}")
        flash(f"Error: {e}", 'danger')
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=('GET', 'POST'))
def update_employee(id):
    employee = db.get_one(id)
    if request.method == 'POST':
        err = validate_form(request.form)
        if err:
            flash(err, 'danger')
            return redirect(url_for('update_employee', id=id))

        data = (
            request.form.get('name'), request.form.get('email'), request.form.get('age'),
            request.form.get('gender'), request.form.get('marital_status'), request.form.get('department'),
            request.form.get('job_role'), request.form.get('salary'), request.form.get('experience'),
            request.form.get('job_level'), id
        )
        try:
            db.update(data)
            logging.info(f"Successfully updated record ID: {id}.")
            flash(f"Successfully updated record", 'success')
            return redirect(url_for('update_employee', id=id))
        except Exception as e:
            logging.error(f"Update Error: {e}")
            flash(f"Error: {e}", 'danger')
    return render_template('update.html', emp=employee)

@app.route('/download')
def download_csv():
    logging.info("Transforming Data for CSV Download.")
    employees = db.get_all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['emp_id', 'name', 'email', 'age', 'gender', 'marital_status', 
                     'department', 'job_role', 'salary', 'experience', 'job_level'])
    for emp in employees:
        writer.writerow(list(emp))
    
    logging.info(f"Successfully exported {len(employees)} records.")
    output.seek(0)
    return Response(output.getvalue(), mimetype="text/csv", 
                    headers={"Content-disposition": "attachment; filename=employees.csv"})

if __name__ == '__main__':
    logging.info("Starting Server at http://127.0.0.1:5000")
    app.run(debug=False, host='0.0.0.0')
    

