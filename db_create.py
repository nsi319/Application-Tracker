# import sqlite3
# from models import Candidate
# import nltk
# import shutil,os
# import psycopg2
# # nltk.download('punkt')
# # nltk.download('averaged_perceptron_tagger')
# # nltk.download('maxent_ne_chunker')
# # nltk.download('words')
# # nltk.download('wordnet')
# conn = psycopg2.connect(host="ec2-52-73-247-67.compute-1.amazonaws.com",database="dbd27anbkuq3m2", user="qkeebbeasjwfud", password="eeaf29f8b54c1471d9c68620f1d91b0612e702b1233e8b8688aeba67056f2060")
# cur = conn.cursor()
# print("Opened database successfully")
# #conn.execute('DROP TABLE candidate')
# cur.execute('CREATE TABLE candidate (phone TEXT,email TEXT,linkedin TEXT,exp_years TEXT, duration TEXT,summary TEXT,skills TEXT,experience TEXT,education TEXT,extra TEXT,awards TEXT,filename TEXT, complete_resume TEXT, resume VARCHAR(500) PRIMARY KEY)')
# print("Table created successfully")
# cur.close()
# dire = 'assets'
# if os.path.exists(os.path.abspath(dire)):
#     shutil.rmtree(dire)
# os.makedirs(os.path.abspath(dire))

# dire = 'all_resumes'
# if os.path.exists(os.path.abspath(dire)):
#     shutil.rmtree(dire)
# os.makedirs(os.path.abspath(dire))

# print("created new dirs")

# conn.close()


from app import db
from models import Candidate

db.create_all()
first = ['hello','naren',['hey'],'hola',['duration','is']]
second = ['h','l','k','a','b','p']
cand = Candidate(email=str(first[0]),linkedin=first[1],phone=first[2][0],exp_years=first[3],duration=" | ".join(first[4]),summary=second[0],skills=second[1],experience=second[2],education=second[3],extra=second[4],awards=second[5],resume='resume',filename='filename',complete_resume='comp_res')
db.session.add(cand)
db.session.commit()
print("Added user naren")