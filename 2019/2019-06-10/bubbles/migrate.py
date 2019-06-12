import bubbles
from bubbles import open_store
from bubbles.metadata import Field
import sqlalchemy
import time

# SQLite DB path
sqlite_path = '/home/fracpete/development/projects/employees-db-sqlite/employees_db-full-1.0.6.db'

# MySQL database
mysql_host = 'localhost'
mysql_db = 'employees_new'
mysql_user = 'migration'
mysql_pw = 'migration'

# directory with social media CSV file
csv_dir = '../data'

# the tables to migrate
tables = [
    'departments',
    'dept_emp',
    'dept_manager',
    'employees',
    'salaries',
    'titles',
]

start_time = time.time()

# connect to databases
sqlite_store = open_store(
        'sql', 
        'sqlite:////' + sqlite_path)
mysql_store = open_store(
        'sql', 
        'mysql+mysqldb://' + mysql_user + ':' + mysql_pw + '@' + mysql_host + '/' + mysql_db)
csv_store = open_store(
        'csv',
        csv_dir)

# migrate tables
for table in tables:
    print(table)
    sqlite_obj = sqlite_store.get_object(table)
    fields = sqlite_obj.fields
    # add email column
    if table == 'employees':
        email_field = Field(name='email', storage_type='string', size=255) 
        fields.append(email_field)
    mysql_obj = mysql_store.create(table, fields)
    for row in sqlite_obj.rows():
        # construct email
        if table == 'employees':
            ln = row['last_name']
            fn = row['first_name']
            email = fn + "." + ln + "@mycompany.com"
            # TODO how add???
        mysql_obj.append(row)
    mysql_obj.flush()

# import socialmedia
csv_obj = csv_store.get_object('socialmedia.csv')
fields = csv_obj.fields
for field in fields:
    # to avoid exception: "VARCHAR requires a length on dialect %s" % self.dialect.name
    if field.storage_type == 'string':
        field.size = 255
empno_field = Field(name='emp_no', storage_type='integer')
fields.append(empno_field)
mysql_obj = mysql_store.create('socialmedia', fields)
for row in csv_obj.rows():
    # TODO run SQL query to get emp_no
    mysql_obj.append(row)
mysql_obj.flush()

end_time = time.time()
print("execution time", end_time - start_time)
    
