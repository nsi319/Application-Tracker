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
        __tablename__ = "users"
        id = db.Column(db.Integer,nullable=False,primary_key=True)
        username = db.Column(db.Text,nullable=False)
        password = db.Column(db.Text,nullable=False)
        usertype = db.Column(db.Text,nullable=False)

def init_db():
    db.create_all()
    # Create a test user
    new_user = User(1,'a@a.com', 'aaaaaaaa')
    db.session.add(new_user)
    db.session.commit()

if __name__ == '__main__':
    init_db()
