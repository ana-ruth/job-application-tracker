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

'''
    Companies Table
'''

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


'''
    Contacts Table
'''

@app.route('/contacts')
def contacts():

    edit_id = request.args.get('edit', type=int)    
    conn = get_db() 
    cursor = conn.cursor(dictionary=True) 
    
    contacts = read_all_contacts()

    #GET companies for companies dropdown in insert contact form
    cursor.execute('SELECT company_id, company_name FROM companies')
    companies = cursor.fetchall()
    
    cursor.close
    conn.close()


    return render_template('contacts.html', contacts=contacts, companies=companies, edit_id=edit_id)


@app.route('/contacts/insert', methods=['GET','POST'])
def createContacts():
 
    # if user input is empty set it to None (Null)
    company_id = request.form['company_id'] or None
    first_name = request.form['first_name'].strip() or None
    last_name =  request.form['last_name'].strip() or None
    email = request.form['email'].strip() or None
    phone = request.form['phone'].strip() or None
    job_title = request.form['job_title'].strip() or None
    linkedin_url = request.form['linkedin_url'].strip() or None
    notes = request.form['notes'].strip() or None

    create_contact(company_id, first_name, last_name,email, phone, job_title, linkedin_url, notes)

    return redirect('/contacts')

@app.route('/contacts/delete', methods=['POST'])
def deleteContact():
    if request.method == 'POST':
        contactID = request.form['contact_id'] 
        delete_contact(contactID) 
    return redirect('/contacts')


@app.route('/contacts/update/<int:contact_id>', methods = ['POST'])
def updateContact(contact_id):
   
    # if user input is empty set it to None (Null)
    
    company_id = request.form.get('company_id') 
    first_name = request.form.get('first_name','').strip() or None
    last_name = request.form.get('last_name','').strip() or None
    email = request.form.get('email','').strip() or None
    phone = request.form.get('phone','').strip() or None
    job_title = request.form.get('job_title','').strip() or None
    linkedin_url = request.form.get('linkedin_url','').strip() or None
    notes = request.form.get('notes','').strip() or None

    update_contact(contact_id, company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes)
      
    return redirect(url_for('contacts'))


'''
    Jobs Table
'''
@app.route('/jobs')
def jobs():

    edit_id = request.args.get('edit', type=int)    
    conn = get_db() 
    cursor = conn.cursor(dictionary=True) 
    
    jobs = read_all_jobs()

    #GET companies for companies dropdown in insert job form
    cursor.execute('SELECT company_id, company_name FROM companies')
    companies = cursor.fetchall()
    
    cursor.close
    conn.close()


    return render_template('jobs.html', jobs=jobs, companies=companies, edit_id=edit_id)


if __name__ == '__main__':
    app.run(debug=True)