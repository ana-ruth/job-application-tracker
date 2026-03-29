from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

from database import *
import json

app = Flask(__name__)

def get_db():
    return mysql.connector.connect(
        host='localhost', user='root',
        password='root123;', database='job_tracker'
    )


'''
    Dashboard
'''

@app.route('/')
def dashboard():
    stats = statistics()
    return render_template('dashboard.html', stats=stats)



'''
    Companies Table
        functions: companies(), updateCompany(), deleteCompany(), createCompany()
'''

@app.route('/companies')
def companies():

    edit_id = request.args.get('edit', type=int)
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
        functions: contacts(), createContacts(), deleteContact(), updateContact()
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
        functions: jobs(), deleteJob(), createJob(), updateJob()
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


@app.route('/jobs/delete', methods=['POST'])
def deleteJob():
    if request.method == 'POST':
        jobID = request.form['job_id'] 
        delete_job(jobID) 
    return redirect('/jobs')


@app.route('/jobs/insert', methods=['GET','POST'])
def createJob():
 
    # if user input is empty set it to None (Null)
    company_id = request.form['company_id'] or None
    job_title = request.form['job_title'].strip() or None
    job_description =  request.form['job_description'].strip() or None
    salary_min = request.form['salary_min'].strip() or None
    salary_max = request.form['salary_max'].strip() or None
    job_type = request.form['job_type'].strip() or None
    job_url = request.form['job_url'].strip() or None
    date_posted = request.form['date_posted'].strip() or None
    is_active = request.form['is_active'].strip() or None
    
    # JSON Column
    raw_text = request.form.get('requirements', '')
    requirements_dict = {}

    # Split the text into individual lines
    lines = raw_text.strip().split('\n')
    
    for line in lines:
        if ':' in line:
            # Split the line at the first colon
            key, value = line.split(':', 1)
            k = key.strip()
            v = value.strip()
            
            if k and v:
                if v.isdigit():
                    requirements_dict[k] = int(v)
                elif k.lower() == 'required_skills' or k.lower() == 'skills' or ',' in v:
                    requirements_dict[k] = [i.strip() for i in v.split(',') if i.strip()]
                else:
                    requirements_dict[k] = v

    requirements = json.dumps(requirements_dict)


    create_job(company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements)

    return redirect('/jobs')

@app.route('/jobs/update/<int:job_id>', methods = ['POST'])
def updateJob(job_id):
   
    # if user input is empty set it to None (Null)
    company_id = request.form.get('company_id') 
    job_title = request.form.get('job_title','').strip() or None
    job_description = request.form.get('job_description','').strip() or None
    salary_min = request.form.get('salary_min','').strip() or None
    salary_max = request.form.get('salary_max','').strip() or None
    job_type = request.form.get('job_type','').strip() or None
    job_url = request.form.get('job_url','').strip() or None
    date_posted = request.form.get('date_posted','').strip() or None
    is_active = request.form.get('is_active','').strip() or None
    
    #requirements_data JSON column
    raw_text = request.form.get('requirements', '')
    requirements_dict = {}
    
    # Split text into lines and process each "Key: Value" pair
    for line in raw_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            k = key.strip()
            v = val.strip()
            
            if k and v:
                if v.isdigit():
                    requirements_dict[k] = int(v)
                elif k.lower() == 'required_skills' or k.lower() == 'skills' or ',' in v:
                    requirements_dict[k] = [i.strip() for i in v.split(',') if i.strip()]
                else:
                    requirements_dict[k] = v

    requirements = json.dumps(requirements_dict)

    update_job(job_id, company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements)
      
    return redirect(url_for('jobs'))




'''
    Applications Table
        functions: applications(), createApplication(), deleteApplication(), updateApplication()
'''

@app.route('/applications')
def applications():
    edit_id = request.args.get('edit', type=int)    
    conn = get_db() 
    cursor = conn.cursor(dictionary=True) 
    
    applications = read_all_applications()

    #GET companies for companies dropdown in insert application form
    cursor.execute('SELECT company_id, company_name FROM companies')
    companies = cursor.fetchall()

    #GET jobs for jobs dropdown in insert application form
    cursor.execute('SELECT job_id, job_title FROM jobs')
    jobs = cursor.fetchall()
    
    cursor.close
    conn.close()


    return render_template('applications.html', applications=applications, companies=companies, jobs=jobs, edit_id=edit_id)


@app.route('/applications/insert', methods=['GET','POST'])
def createApplication():

    #interview data JSON column
    raw_text = request.form.get('interview_data', '')
    interview_dict = {}

    # Split the text into individual lines
    lines = raw_text.strip().split('\n')
    
    for line in lines:
        if ':' in line:
            # Split the line at the first colon
            key, value = line.split(':', 1)
            k = key.strip()
            v = value.strip()
            
            if k and v:
                if v.isdigit():
                    interview_dict[k] = int(v)
                elif k.lower() == 'interviewers' or k.lower() == 'skills' or k.lower() == 'technical_questions' or ',' in v:
                    interview_dict[k] = [i.strip() for i in v.split(',') if i.strip()]
                else:
                    interview_dict[k] = v

    interview_data = json.dumps(interview_dict)

    # if user input is empty set it to None (Null)
    job_id = request.form['job_id'] or None
    application_date =  request.form['application_date'].strip() or None
    status = request.form['status'].strip() or None
    resume_version = request.form['resume_version'].strip() or None
    cover_letter_sent = request.form['cover_letter_sent'].strip() or None
    response_date = request.form['response_date'].strip() or None
    interview_date = request.form['interview_date'].strip() or None
    notes = request.form['notes'].strip() or None


    create_application(job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data)

    return redirect('/applications')



@app.route('/applications/delete', methods=['POST'])
def deleteApplication():
    if request.method == 'POST':
        applicationID = request.form['application_id'] 
        delete_application(applicationID) 
    return redirect('/applications')

@app.route('/applications/update/<int:application_id>', methods = ['POST'])
def updateApplication(application_id):
   
    # if user input is empty set it to None (Null)
    company_id = request.form.get('company_id') 
    job_id = request.form.get('job_id','')

    application_date = request.form.get('application_date','').strip() or None
    status = request.form.get('status','').strip() or None
    resume_version = request.form.get('resume_version','').strip() or None
    cover_letter_sent = request.form.get('cover_letter_sent','').strip() or None
    response_date = request.form.get('response_date','').strip() or None
    interview_date = request.form.get('interview_date','').strip() or None
    notes = request.form.get('notes','').strip() or None

    #interview_data JSON column
    raw_text = request.form.get('interview_raw', '')
    interview_dict = {}
    
    # Split text into lines and process each "Key: Value" pair
    for line in raw_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            k = key.strip()
            v = val.strip()
            
            if k and v:
                if v.isdigit():
                    interview_dict[k] = int(v)
                elif any(word in k.lower() for word in ['interviewer', 'skill', 'member']):
                    interview_dict[k] = [i.strip() for i in v.split(',') if i.strip()]
                else:
                    interview_dict[k] = v

    interview_data = json.dumps(interview_dict)

    update_application(application_id, job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data)
      
    return redirect(url_for('applications'))



'''
    Job Match
        functions: find_jobs(), job_match()
'''
@app.route('/job_match', methods=['GET','POST'])
def find_jobs():

    raw_input = request.form.get('skills', '')
    user_skills = [s.strip() for s in raw_input.split(',') if s.strip()]


    jobs = read_all_active_jobs()

    results = []
    for job in jobs:
        score, missing = job_match(user_skills, job["required_skills"])        

        match_count = len(job["required_skills"]) - len(missing)
        total_skills = len(job["required_skills"])

        # only include jobs where at least 1 skill is matched
        if score > 0:
            results.append({
                'title': job['job_title'],
                'company_name': job['company_name'],
                'match_percent': score,
                'match_count': match_count,
                'total_skills': total_skills,
                'missing': missing 
                })
            
    jobs = sorted(results, key=lambda x: x['match_percent'], reverse=True)

    return render_template('job_match.html', jobs=jobs, user_skills = user_skills)


def job_match(user_skills, required_skills):

    if not required_skills:
        return 0, user_skills

    matched_skills = []
    missing_skills = []

    lower_required_skills = [s.lower() for s in required_skills]

    # matched skills
    for skill in user_skills:
            if skill.lower() in lower_required_skills:
                matched_skills.append(skill.lower())
 
    # get missing skills
    for skill in required_skills:
        if skill.lower() not in matched_skills:
            missing_skills.append(skill)


    #Calculate percentage of matched skills
    score = int((len(matched_skills) / len(required_skills)) * 100) if len(required_skills) > 0 else 0
    
    return score, missing_skills


if __name__ == '__main__':
    app.run(debug=True)
