from flask import Flask, render_template, request, redirect
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
    companies = read_all_companies()
    return render_template('companies.html', companies=companies)

@app.route('/companies/delete', methods=['POST'])
def deleteCompany():
    if request.method == 'POST':
        company = request.form['Company'] 
        delete_company(company) 
    return redirect('/companies')

@app.route('/companies/update', methods=['POST'])
def updateCompany():
    if request.method == 'POST':
        company = request.form['companyName']
        notes = request.form['CompanyNotes']
        update_company(company, notes)

    return redirect('/companies')

@app.route('/companies/insert', methods=['POST'])
def createCompany():
    if request.method == 'POST':
        company = request.form['company_name'] 
        industry = request.form['industry']
        website =  request.form['website']
        city = request.form['city']
        state = request.form['state']
        notes = request.form['notes']
        
        create_company(company, industry, website,city, state, notes)
    
    return redirect('/companies')


if __name__ == '__main__':
    app.run(debug=True)