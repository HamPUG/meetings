import bonobo
import bonobo_sqlalchemy
from bonobo_sqlalchemy.util create_engine

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
for table in tables:
    print(table)

