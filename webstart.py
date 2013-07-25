
"""
A single page app exmploring how to use SQLAlchemy & Flask.
"""


import os, pdb
from sqlalchemy import distinct, func
from sqlalchemy.orm import scoped_session, sessionmaker
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.debug = False
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
    # note we've not bothered with a template, 
    # and encoding the URL will work both ways in modern browsers 
    # (though encoding w/ %20 is preferable)
    return """<h1>LinkedIn 0.0.0.0.0.0.1</h1>
<pre>
    <a href="/Darrell%20Silver">Darrell</a>
    <a href="/Dan Friedman">Dan</a>
</pre>"""

@app.route('/<name>')
def career_history(name):
    # one strategy for querying
    jobs = Job.query.join(Person).filter(Person.name==name)

    # another querying strategy; more common, but uglier, IMO
    titles = db.session.query(Job.title).join(Person) \
        .filter(Person.name==name).distinct()

    # is this any clearer than raw SQL? Seems silly.
    employers = db.session.query(Company.name, func.count(Company.id)) \
        .join(Job).join(Person) \
        .filter(Person.name==name).group_by(Company.name)

    return render_template('career_history.html', name=name, jobs=jobs, 
        titles=titles, employers=employers)

def main():
    print 'Dropping all...'
    db.drop_all()
    print 'Creating all...'
    db.create_all()
    setup_darrell()
    setup_dan()
    print 'Starting app...'
    app.run()

if __name__ == '__main__':
    main()

