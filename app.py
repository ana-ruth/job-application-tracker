from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

from database import *

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host='localhost', user='root',
        password='root123;', database='job_tracker'
    )

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', stats=stats)

@app.route('/companies')
def companies():

    edit_id = request.args.get('edit', type=int)    
    conn = get_db() 
    cursor = conn.cursor(dictionary=True) 
    cursor.close
    companies = read_all_companies()

    return render_template('companies.html', companies=companies, edit_id=edit_id)


@app.route('/companies/update/<int:company_id>', methods = ['POST'])
def updateCompany(company_id):
   
    # if user input is empty set it to None (Null)
    company_name = request.form.get('company_name') 
    industry = request.form.get('industry','').strip() or None
    website = request.form.get('website','').strip() or None
    city = request.form.get('city','').strip() or None
    state = request.form.get('state','').strip() or None
    notes = request.form.get('notes','').strip() or None

    update_company(company_id, company_name, industry, website, city, state, notes)
      
    return redirect(url_for('companies'))




@app.route('/companies/delete', methods=['POST'])
def deleteCompany():
    if request.method == 'POST':
        companyID = request.form['company_id'] 
        delete_company(companyID) 
    return redirect('/companies')


@app.route('/companies/insert', methods=['POST'])
def createCompany():
    if request.method == 'POST':

        # if user input is empty set it to None (Null)
        company = request.form['company_name'] 
        industry = request.form['industry'].strip() or None
        website =  request.form['website'].strip() or None
        city = request.form['city'].strip() or None
        state = request.form['state'].strip() or None
        notes = request.form['notes'].strip() or None

        create_company(company, industry, website,city, state, notes)
    
    return redirect('/companies')


if __name__ == '__main__':
    app.run(debug=True)