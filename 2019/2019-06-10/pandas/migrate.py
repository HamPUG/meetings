import pandas as pd
from sqlalchemy import create_engine
import MySQLdb

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

# connect to mysql
mysql_engine = create_engine(
    'mysql+mysqldb://' + mysql_user + ':' + mysql_pw + '@' + mysql_host + '/' + mysql_db)

# connect to sqlite
sqlite_engine = create_engine('sqlite:///' + sqlite_path)

# migrate tables
with sqlite_engine.connect() as sqlite_conn, sqlite_conn.begin():
    pass
    for table in tables:
        print(table)
        # read
        data = pd.read_sql_table(table, sqlite_conn)
        # add 'email' column to 'employees'
        if table == 'employees':
            emails = []
            ln = data['last_name']
            fn = data['first_name']
            for i in range(len(ln)):
                emails.append(fn[i] + '.' + ln[i] + '@mycompany.com')
            data['email'] = emails
        # write
        data.to_sql(table, con=mysql_engine, index=False, if_exists='replace')

# read social media
print('socialmedia')
data = pd.read_csv(socialmedia_csv, sep=',')
# add employee_no
ln = data['last_name']
fn = data['first_name']
bd = data['birth_date']
emp_nos = []
for i in range(len(ln)):
    sub = pd.read_sql_query(
            "SELECT emp_no FROM employees " 
            + "where last_name = '" + ln[i] + "' "
            + "and first_name = '" + fn[i] + "' "
            + "and birth_date = '" + bd[i] + "' "
            + "order by birth_date desc "
            + "limit 1", 
            sqlite_engine)
    if len(sub['emp_no'] > 0):
        emp_nos.append(sub['emp_no'][0])
    else:
        emp_nos.append(-1)
data['emp_no'] = emp_nos
# write
data.to_sql('socialmedia', con=mysql_engine, index=False, if_exists='replace')

# close connections
sqlite_conn.close()
# MySQL automatically closes

