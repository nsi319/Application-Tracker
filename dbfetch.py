from models import *
from app import db
cand = Candidate.query.all()
for c in cand:
    file1 = open("data1.txt","w")#write mode 
    file1.write(c.complete_resume) 
    file1.close()
