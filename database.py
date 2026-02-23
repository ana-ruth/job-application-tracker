import mysql.connector
from app import get_db

config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root123;',
    'database': 'job_tracker'
}

def read_all_companies():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM companies')
    companies = cursor.fetchall()
    conn.close()

    return companies
