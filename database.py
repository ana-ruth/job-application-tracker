import mysql.connector
from app import get_db

import json

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123;',
    'database': 'job_tracker'
}

'''
    Dashboard 
'''

def statistics():
    try:
        stats = {}

        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        
        # Get application and overall statistics from tables
        query = """
                SELECT 
                    (SELECT COUNT(*) FROM jobs) AS total_jobs,
                    (SELECT COUNT(*) FROM companies) AS total_companies,
                    (SELECT COUNT(*) FROM contacts) AS total_contacts,
                    COUNT(*) AS total_applications,
                    COALESCE(SUM(CASE WHEN status = 'Applied' THEN 1 ELSE 0 END), 0) AS s_applied,
                    COALESCE(SUM(CASE WHEN status = 'Screening' THEN 1 ELSE 0 END), 0) AS s_screening,
                    COALESCE(SUM(CASE WHEN status = 'Phone Screen' THEN 1 ELSE 0 END), 0) AS s_phone,
                    COALESCE(SUM(CASE WHEN status = 'Interview' THEN 1 ELSE 0 END), 0) AS s_interview,
                    COALESCE(SUM(CASE WHEN status = 'Interview Completed' THEN 1 ELSE 0 END), 0) AS s_completed,
                    COALESCE(SUM(CASE WHEN status = 'Offer' THEN 1 ELSE 0 END), 0) AS s_offer,
                    COALESCE(SUM(CASE WHEN status = 'Offer Accepted' THEN 1 ELSE 0 END), 0) AS s_accepted,
                    COALESCE(SUM(CASE WHEN status = 'Rejected' THEN 1 ELSE 0 END), 0) AS s_rejected,
                    COALESCE(SUM(CASE WHEN status = 'Withdrawn' THEN 1 ELSE 0 END), 0) AS s_withdrawn
                FROM applications;
            """
        
        cursor.execute(query)
        stats = cursor.fetchone()


        conn.close()

        return stats
        
    except mysql.connector.Error as error:
        print(f'Error Fetching Statistics: {error}')
        conn.rollback()



'''
    Companies Table
        functions: read_all_companies, delete_company, update_company, create_company
'''
def read_all_companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies') # Select all companies
    companies = cursor.fetchall()
    conn.close()
    return companies

def delete_company(company_id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Delete selected company
        delete_query = 'DELETE FROM companies WHERE company_id = %s'
        cursor.execute(delete_query, (company_id,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error Deleting Company: {error}')
        conn.rollback()

def update_company(company_id, company_name, industry, website, city, state, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   

        # Update selected company
        update_query = 'UPDATE companies SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s WHERE company_id = %s'
        cursor.execute(update_query, (company_name, industry, website, city, state, notes, company_id))
        
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Company: {error}')
        conn.rollback()

def create_company(company_name, industry, website, city, state, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   

        # Insert new company
        insert_query = '''INSERT INTO companies (company_name, industry, website, city, state, notes) 
                           VALUES (%s, %s, %s, %s, %s, %s)
                       '''
        values = (company_name, industry, website, city, state, notes)
        cursor.execute(insert_query, values)
        conn.commit()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f'Error Inserting Company: {error}')
        conn.rollback()


'''
    Contacts Table
        functions: read_all_contacts, create_contact, delete_contact, update_contact
'''

def read_all_contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Select all contacts and their corresponding companies
    cursor.execute("""
                   SELECT c.*, co.company_name 
                   FROM contacts c 
                   LEFT JOIN companies co ON c.company_id = co.company_id
        """)
    
    
    contacts = cursor.fetchall()
    conn.close()

    return contacts

def create_contact(company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True) 

        # Insert new contact  
        insert_query = '''INSERT INTO contacts (company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                       '''
        values = (company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes)
        cursor.execute(insert_query, values)
        conn.commit()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f'Error Inserting Contact: {error}')
        conn.rollback()

def delete_contact(contactID):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Delete selected contact
        delete_query = 'DELETE FROM contacts WHERE contact_id = %s'
        cursor.execute(delete_query, (contactID,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error Deleting Contact: {error}')
        conn.rollback()

def update_contact(contact_id, company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   

        # Update selected contact
        update_query = 'UPDATE contacts SET company_id = %s, first_name = %s, last_name = %s, email = %s, phone = %s, job_title = %s, linkedin_url = %s, notes = %s WHERE contact_id = %s'
        cursor.execute(update_query, (company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes, contact_id))
        
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Contact: {error}')
        conn.rollback()


'''
    Jobs Table
        functions: read_all_jobs, read_all_active_jobs, delete_job, create_job, update_job
'''

def read_all_jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Select all jobs and their corresponding company
    cursor.execute("""
                   SELECT j.*, co.company_name 
                   FROM jobs j 
                   LEFT JOIN companies co ON j.company_id = co.company_id
        """)
    
    jobs = cursor.fetchall()
    conn.close()

    # handle JSON column
    for job in jobs:
        if job['requirements']:
            try:
                if isinstance(job['requirements'], str):
                    job['requirements'] = json.loads(job['requirements'])
            except (ValueError, TypeError):
                job['requirements'] = {}
        else:
            job['requirements'] = {}

    return jobs

def read_all_active_jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT j.*, co.company_name, requirements->'$.required_skills' AS required_skills 
                   FROM jobs j 
                   LEFT JOIN companies co ON j.company_id = co.company_id
                   WHERE is_active = 1
        """)
    
    jobs = cursor.fetchall()
    conn.close()

    for job in jobs:
            if job['required_skills']:
                # Turn the JSON string from MySQL into a Python List
                job['required_skills'] = json.loads(job['required_skills'])
            else:
                job['required_skills'] = []

    return jobs

def delete_job(jobID):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Delete selected job
        delete_query = 'DELETE FROM jobs WHERE job_id = %s'
        cursor.execute(delete_query, (jobID,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error Deleting Job: {error}')
        conn.rollback()

def create_job(company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Insert new job   
        insert_query = '''INSERT INTO jobs (company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                       '''
        values = (company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements)
        cursor.execute(insert_query, values)
        conn.commit()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f'Error Inserting Job: {error}')
        conn.rollback()



def update_job(job_id, company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)  

        # Update selected job 
        update_query = 'UPDATE jobs SET company_id = %s, job_title = %s, job_description = %s, salary_min = %s, salary_max = %s, job_type = %s, job_url = %s, date_posted = %s, is_active = %s, requirements = %s WHERE job_id = %s'
        cursor.execute(update_query, (company_id, job_title, job_description, salary_min, salary_max, job_type, job_url, date_posted, is_active, requirements, job_id))
       
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Job: {error}')
        conn.rollback()


'''
    Applications Table
        functions: read_all_applications, create_application, delete_application, update_application, 
'''
def read_all_applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)

    # Select all applications and their corresponding company and job
    cursor.execute("""
                   SELECT a.*, c.company_name, j.job_title 
                   FROM applications a 
                   LEFT JOIN jobs j ON j.job_id = a.job_id
                   LEFT JOIN companies c ON j.company_id = c.company_id
        """)
    
    applications = cursor.fetchall()
    conn.close()

    for app in applications:
        if app.get('interview_data'):
            try:
                # Convert JSON to dictionary
                app['interview_data'] = json.loads(app['interview_data'])
            except (json.JSONDecodeError, TypeError):
                app['interview_data'] = {}
        else:
            app['interview_data'] = {}

    return applications

def create_application(job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   

        # Insert new application
        insert_query = '''INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    '''
        values = (job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data)
        cursor.execute(insert_query, values)
        conn.commit()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f'Error Inserting Application: {error}')
        conn.rollback()

def delete_application(applicationID):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)

        # Delete selected application
        delete_query = 'DELETE FROM applications WHERE application_id = %s'
        cursor.execute(delete_query, (applicationID,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error Deleting Applications: {error}')
        conn.rollback()


def update_application(application_id, job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   

        # Update selected application
        update_query = 'UPDATE applications SET job_id = %s, application_date = %s, status = %s, resume_version = %s, cover_letter_sent = %s, response_date = %s, interview_date = %s, notes = %s, interview_data = %s WHERE application_id = %s'
        cursor.execute(update_query, (job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, interview_data, application_id))
        
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Application: {error}')
        conn.rollback()