import sqlite3
from models import Candidate
import nltk
import shutil,os


conn = sqlite3.connect('ats.db')
print("Opened Candidate database successfully")


conn.execute('CREATE TABLE if not exists candidate (phone TEXT,email TEXT,linkedin TEXT,exp_years TEXT, duration TEXT,summary TEXT,skills TEXT,experience TEXT,education TEXT,extra TEXT,awards,filename TEXT, complete_resume TEXT, resume STRING(500) PRIMARY KEY)')
print("Candidate Table created successfully")

conn.execute('''
create table user(
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

