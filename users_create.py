import sqlite3
from models import User
import nltk
import shutil,os
conn = sqlite3.connect('Candidate.db')
print("Opened database successfully")
#conn.execute('DROP TABLE candidate')
conn.execute('CREATE TABLE users(id INT,username text,password text')
print("Table created successfully")

dire = 'assets'
if os.path.exists(os.path.abspath(dire)):
    shutil.rmtree(dire)
os.makedirs(os.path.abspath(dire))

dire = 'all_resumes'
if os.path.exists(os.path.abspath(dire)):
    shutil.rmtree(dire)
os.makedirs(os.path.abspath(dire))

print("created new dirs")

conn.close()