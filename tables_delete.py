from models import *
from app import db
cand = Candidate.query.all()
for c in cand:
    db.session.delete(c)
    db.session.commit()
    