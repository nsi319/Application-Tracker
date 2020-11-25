import sqlite3
import nltk
import shutil,os


conn = sqlite3.connect('ats.db')
conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(1,"Google",0,"Google",'M',"","pref",0,"resume_path","123456",'company'))
conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(2,"Amazon",0,"Amazon",'M',"","pref",0,"resume_path","123456",'company'))
conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(3,"Microsoft",0,"Microsoft",'M',"","pref",0,"resume_path","123456",'company'))
conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(4,"Facebook",0,"Facebook",'M',"","pref",0,"resume_path","123456",'company'))
conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(5,"Oracle",0,"Oracle",'M',"","pref",0,"resume_path","123456",'company'))
conn.execute('insert into user values (?,?,?,?,?,?,?,?,?,?,?)',(6,"Fidelity",0,"Fidelity",'M',"","pref",0,"resume_path","123456",'company'))


print("application table created")

conn.close()

