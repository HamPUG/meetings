import petl as etl
import sqlite3
import pymysql

# SQLite DB path
sqlite_path = '/home/fracpete/development/projects/employees-db-sqlite/employees_db-full-1.0.6.db'

# MySQL database
mysql_host = 'localhost'
mysql_db = 'employees_new'
mysql_user = 'migration'
mysql_pw = 'migration'

# social media CSV file
socialmedia_csv = '../data/socialmedia.csv'

# the tables to migrate
tables = [
    'departments',
    'dept_emp',
    'dept_manager',
    'employees',
    'salaries',
    'titles',
]

# connect to sqlite
sqlite_conn = sqlite3.connect(sqlite_path)

# connect to mysql
mysql_conn = pymysql.connect(host=mysql_host, database=mysql_db, user=mysql_user, password=mysql_pw)
mysql_conn.cursor().execute('SET SQL_MODE=ANSI_QUOTES')

# migrate tables
for table in tables:
    print(table)
    data = etl.fromdb(sqlite_conn, 'select * from ' + table)
    if table == 'employees':
        recs = etl.records(data)
        emails = []
        for rec in recs:
            emails.append(rec['first_name'] + '.' + rec['last_name'] + '@mycompany.com')
        data2 = etl.addcolumn(data, 'email', emails)
    else:
        data2 = data
    etl.todb(data2, mysql_conn, table, create=True)

# load CSV file
data = etl.fromcsv(source=socialmedia_csv)
recs = etl.records(data)
# determine employee numbers
empnos = []
for rec in recs:
    sub = etl.fromdb(
            sqlite_conn,
            "SELECT emp_no FROM employees " 
            + "where last_name = '" + rec['last_name'] + "' "
            + "and first_name = '" + rec['first_name'] + "' "
            + "and birth_date = '" + rec['birth_date'] + "' "
            + "order by birth_date desc "
            + "limit 1")
    vals = etl.values(sub, 'emp_no')
    if len(vals) > 0:
        empnos.append(vals[0])
    else:
        empnos.append(-1) # dummy
# adding column gets ignored??
data2 = etl.addcolumn(data, 'emp_no', empnos)
etl.todb(data2, mysql_conn, 'socialmedia', create=True)

# close connections
sqlite_conn.close()

