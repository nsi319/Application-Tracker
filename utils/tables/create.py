import sqlite3
import sys
sys.path.insert(0,'../..')
from models import Candidate
import nltk
import shutil,os
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('wordnet')
# open('../../Candidate.db','a').close()

conn = sqlite3.connect('/app/Candidate.db')
print("Opened database successfully")
conn.execute('DROP TABLE if exists candidate')
conn.execute('CREATE TABLE candidate (phone TEXT,email TEXT,linkedin TEXT,exp_years TEXT, duration TEXT,summary TEXT,skills TEXT,experience TEXT,education TEXT,extra TEXT,awards,filename TEXT, complete_resume TEXT, resume STRING(500) PRIMARY KEY)')
print("Table created successfully")

dire = '/app/assets'
if os.path.exists(os.path.abspath(dire)):
    shutil.rmtree(dire)
    print("Yes assets existed")
os.makedirs(os.path.abspath(dire))

dire = '/app/all_resumes'
if os.path.exists(os.path.abspath(dire)):
    shutil.rmtree(dire)
    print("Yes all_resumes existed")

os.makedirs(os.path.abspath(dire))

cand = Candidate.query.all()
print(cand)


print("Created table and new directories")

conn.close()