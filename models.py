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
    

class User(db.Model):
        __bind_key__ = 'user'
        __tablename__ = "user"
        id = db.Column(db.Integer,nullable=False,primary_key=True)
        username = db.Column(db.Text,nullable=False)
        age = db.Column(db.Text)
        name = db.Column(db.Text)
        sex = db.Column(db.Text)
        domain = db.Column(db.Text)
        pref = db.Column(db.Text)
        exp = db.Column(db.Text)
        resume_path = db.Column(db.Text)
        password = db.Column(db.Text,nullable=False)
        usertype = db.Column(db.Text,nullable=False)

