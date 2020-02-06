from models import Candidate
import sqlite3

conn = sqlite3.connect('Candidate.db')
cur = conn.cursor()
cur.execute('select * from candidate')
cand = cur.fetchall()
print("total cand",len(cand))
for c in cand:
    print(c[1])

conn.execute('delete from candidate')
print("contents deleted \n")

cur.execute('select * from candidate')
cand = cur.fetchall()
print("total cand",len(cand))
conn.close()