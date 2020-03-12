import sqlite3
from models import Candidate
import nltk
import shutil,os
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('maxent_ne_chunker')
# nltk.download('words')
# nltk.download('wordnet')
conn = sqlite3.connect('Candidate.db')
print("Opened database successfully")
#conn.execute('DROP TABLE candidate')
conn.execute('CREATE TABLE candidate (phone TEXT,email TEXT,linkedin TEXT,exp_years TEXT, duration TEXT,summary TEXT,skills TEXT,experience TEXT,education TEXT,extra TEXT,awards,filename TEXT, complete_resume TEXT, resume STRING(500) PRIMARY KEY)')
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