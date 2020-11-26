import sqlite3
import nltk
import shutil,os


conn = sqlite3.connect('ats.db')
print("Opened Candidate database successfully")

# conn.execute("DROP TABLE candidate");
conn.execute('CREATE TABLE if not exists candidate (id int primary key, phone TEXT,email TEXT,linkedin TEXT,exp_years TEXT, duration TEXT,summary TEXT,skills TEXT,experience TEXT,education TEXT,extra TEXT,awards,filename TEXT, complete_resume TEXT, resume STRING(500), foreign key(id) references user(id))')
print("Candidate Table created successfully")

# conn.execute("DROP TABLE user");
conn.execute('''
create table  if not exists user(
  id int primary key,
  username varchar(100),
  age varchar(2),
  name varchar(100),
  sex varchar(1),
  domain varchar(20),
  pref varchar(30),
  exp varchar(30),
  resume_path varchar(200),
  password varchar(100),
  usertype varchar(100)
)''')

print("users table created")

# conn.execute("DROP TABLE job_description");
conn.execute('create table if not exists job_description(id int primary key,domain varchar(20),title varchar(35),desc varchar(50), salary int(15),working_hours int(5),experience int(5),education varchar(30),post_date date, company int, skill varchar(70), foreign key(company) references user(id))')
# conn.execute("DROP TABLE application");
conn.execute('create table if not exists application(id int,job_id int, cand_id int, date_applied date, status varchar(20), foreign key(cand_id) references user(id),foreign key(job_id) references job_description(id))')

print("job and appl table created")

conn.close()

dire = 'assets'
if os.path.exists(os.path.abspath(dire)):
    shutil.rmtree(dire)
os.makedirs(os.path.abspath(dire))

dire = 'all_resumes'
if os.path.exists(os.path.abspath(dire)):
    shutil.rmtree(dire)
os.makedirs(os.path.abspath(dire))

print("created new directories")

