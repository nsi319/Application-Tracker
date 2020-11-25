import sqlite3
from models import Candidate
import nltk
import shutil,os


conn = sqlite3.connect('Candidate.db')
print("Opened Candidate database successfully")
conn.execute('DROP TABLE candidate')
conn.execute('CREATE TABLE candidate (phone TEXT,email TEXT,linkedin TEXT,exp_years TEXT, duration TEXT,summary TEXT,skills TEXT,experience TEXT,education TEXT,extra TEXT,awards,filename TEXT, complete_resume TEXT, resume STRING(500) PRIMARY KEY)')
print("Candidate Table created successfully")
conn.close();


conn = sqlite3.connect('User.db')
print("Opened User database successfully")
conn.execute('DROP TABLE user')
conn.execute('CREATE TABLE user (id INT(100) PRIMARY KEY ,username TEXT,password TEXT,usertype TEXT)')
print("User Table created successfully")
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

