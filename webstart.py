


import os, pdb
from sqlalchemy import distinct, func
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template

def env(name, default=None, required=True):
    value = os.environ.get(name, default)
    if required and not value:
        raise Exception("Missing required environment var '%s'" % name)
    return value


app = Flask(__name__)
app.debug = env("DEBUG", False, False) in ('True', 'true')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/sqlalchemy-demo.db'
db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __repr__(self):
        return self.name

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    # start_date = db.Column(db.DateTime)
    # end_date = db.Column(db.DateTime)

    person_id = db.Column(db.Integer, db.ForeignKey('people.id'))
    person = db.relationship('Person', backref='jobs')
    
    employer_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    employer = db.relationship('Company', backref='staff')

    def __repr__(self):
        return "%s: %s at %s" % (str(self.person), self.title, str(self.employer))

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    # industry_id = db.Column(db.Integer, db.ForeignKey('industries.id'))
    # industry = db.relationship('Course', backref='curriculum_versions')

    def __repr__(self):
        return self.name

def setup_person(name, work_history):
    person = Person(name=name)
    db.session.add(person)
    for company_name, title in work_history:
        employer = Company(name=company_name)
        job = Job(title=title, person=person, employer=employer)
        db.session.add(employer)
        db.session.add(job)

    db.session.commit()

def setup_darrell():
    name = 'Darrell Silver'
    work_history = [
        ('Manhattan Sports', 'Rollerblade salesman'), 
        ('Manhattan Sports', 'Private rollerblade lessons'), 
        ('Vail Resorts', 'Guest Service'), 
        ('Clinton Group', 'Statarb'), 
        ('Perpetually', 'CEO'), 
        ('Thinkful', 'CEO'),
    ]
    setup_person(name, work_history)

def setup_dan():
    name = 'Dan Friedman'
    work_history = [
        ('Dylan\'s Candy Shop', 'Associate'), 
        ('Dylan\'s Candy Shop', 'Finance intern'), 
        ('Ramaquois', 'Camp Counselor'),
        ('RRE', 'Summer analyst'),
        ('Elm City Labs', 'Product manager'),
        ('Thinkful', 'President'),
    ]
    setup_person(name, work_history)

@app.route('/')
def index():
    return render_template('career_history.html', Person=Person, Company=Company, Job=Job,
        func=func, distinct=distinct)

if __name__ == '__main__':
    print 'Dropping all...'
    db.drop_all()
    print 'Creating all...'
    db.create_all()
    setup_darrell()
    setup_dan()
    app.run()
    # pdb.set_trace()


