import mysql.connector
from app import get_db

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123;',
    'database': 'job_tracker'
}

'''
    Companies Table
'''
def read_all_companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies')
    companies = cursor.fetchall()
    conn.close()

    return companies

def delete_company(company_id):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
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
'''

def read_all_contacts():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
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
        update_query = 'UPDATE contacts SET company_id = %s, first_name = %s, last_name = %s, email = %s, phone = %s, job_title = %s, linkedin_url = %s, notes = %s WHERE contact_id = %s'
        
        cursor.execute(update_query, (company_id, first_name, last_name, email, phone, job_title, linkedin_url, notes, contact_id))
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Contact: {error}')
        conn.rollback()


'''
    Jobs Table
'''

def read_all_jobs():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT j.*, co.company_name 
                   FROM jobs j 
                   LEFT JOIN companies co ON j.company_id = co.company_id
        """)
    
    jobs = cursor.fetchall()
    conn.close()

    return jobs

def delete_job(jobID):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        delete_query = 'DELETE FROM jobs WHERE job_id = %s'
        cursor.execute(delete_query, (jobID,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error Deleting Job: {error}')
        conn.rollback()

def create_job(company_id, job_title, job_description, salary_min, salary_max, job_type, posting_url, date_posted, is_active):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   
        insert_query = '''INSERT INTO jobs (company_id, job_title, job_description, salary_min, salary_max, job_type, posting_url, date_posted, is_active) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                       '''
        values = (company_id, job_title, job_description, salary_min, salary_max, job_type, posting_url, date_posted, is_active)
        cursor.execute(insert_query, values)
        conn.commit()
        conn.close()
        
    except mysql.connector.Error as error:
        print(f'Error Inserting Job: {error}')
        conn.rollback()



def update_job(job_id, company_id, job_title, job_description, salary_min, salary_max, job_type, posting_url, date_posted, is_active):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   
        update_query = 'UPDATE jobs SET company_id = %s, job_title = %s, job_description = %s, salary_min = %s, salary_max = %s, job_type = %s, posting_url = %s, date_posted = %s, is_active = %s WHERE job_id = %s'
        
        cursor.execute(update_query, (company_id, job_title, job_description, salary_min, salary_max, job_type, posting_url, date_posted, is_active, job_id))
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Job: {error}')
        conn.rollback()


'''
    Applications Table
'''
def read_all_applications():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
                   SELECT a.*, c.company_name, j.job_title 
                   FROM applications a 
                   LEFT JOIN jobs j ON j.job_id = a.job_id
                   LEFT JOIN companies c ON j.company_id = c.company_id
        """)
    
    applications = cursor.fetchall()
    conn.close()

    return applications

def create_application(job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   
        insert_query = '''INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    '''
        values = (job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes)
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
        delete_query = 'DELETE FROM applications WHERE application_id = %s'
        cursor.execute(delete_query, (applicationID,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error Deleting Applications: {error}')
        conn.rollback()


def update_application(application_id, job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   
        update_query = 'UPDATE applications SET job_id = %s, application_date = %s, status = %s, resume_version = %s, cover_letter_sent = %s, response_date = %s, interview_date = %s, notes = %s WHERE application_id = %s'
        
        cursor.execute(update_query, (job_id, application_date, status, resume_version, cover_letter_sent, response_date, interview_date, notes, application_id))
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error Updating Application: {error}')
        conn.rollback()