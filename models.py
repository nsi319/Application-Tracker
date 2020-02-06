from app import db

class Candidate(db.Model):
    __tablename__="candidate"
    phone = db.Column(db.Text,nullable=False)
    email = db.Column(db.Text,nullable=False)
    linkedin = db.Column(db.Text, nullable=False)
    exp_years = db.Column(db.Text,nullable=False)
    duration = db.Column(db.Text,nullable=False)
    summary = db.Column(db.Text,nullable=False)
    skills = db.Column(db.Text,nullable=False)
    experience = db.Column(db.Text,nullable=False)
    education = db.Column(db.Text,nullable=False)
    extra = db.Column(db.Text,nullable=False)
    awards = db.Column(db.Text,nullable=False)
    resume = db.Column(db.String(500),nullable=False,primary_key=True)
    filename = db.Column(db.Text,nullable=False)
    complete_resume = db.Column(db.Text,nullable=False)

    def __repr__(self):
        return '<Candidate %r>' % self.phone
