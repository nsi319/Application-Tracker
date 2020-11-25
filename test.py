import sqlite3
import nltk
import shutil,os


conn = sqlite3.connect('ats.db')
# conn.execute('alter table job_description rename column job_id to id')
# conn.execute('alter table job_description DROP column post_date')
# conn.execute('alter table job_description add column post_date date')


# conn.execute('create table if not exists job_description(job_id int primary key,domain varchar(20),title varchar(35),desc varchar(50), salary int(15),working_hours int(5),experience int(5),education varchar(30),post_date varchar(20), company int,foreign key(company) references user(id))')
conn.execute('create table if not exists application(id int,job_id int, cand_id int, date_applied varchar(20), status varchar(20), foreign key(cand_id) references user(id),foreign key(job_id) references job_description(id))')

print("application table created")

conn.close()

