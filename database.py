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

def delete_company(company):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)
        delete_query = 'DELETE FROM companies WHERE company_name = %s'
        cursor.execute(delete_query, (company,))
        conn.commit()
        conn.close()

        
    except mysql.connector.Error as error:
        print(f'Error: {error}')
        conn.rollback()

def update_company(company, notes):
    try:
        conn = get_db()
        cursor = conn.cursor(dictionary=True)   
        update_query = 'UPDATE companies SET notes = %s WHERE company_name = %s'
        cursor.execute(update_query, (notes, company))
        conn.commit()
        conn.close()

    except mysql.connector.Error as error:
        print(f'Error: {error}')
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
        print(f'Error: {error}')
        conn.rollback()