# sqlalchemy-demo

## A demonstration of some SQLAlchemy basics.


### In a single file app we
 - create a few related tables using `flask.ext.sqlalchemy`
 - add some data to them
 - query that data using SQLAlchemy
 - display that data in a Jinja2 template rendered in Flask.

### How to run:
 - Simply run `python webstart.py`
 - The app auto-reloads when you make changes to webstart.py, so playing around is super fast.
 - Changes to the template don't require only a web browser refresh (no app reload required!).

### Thoughts:
 - SQLAlchemy makes life unecessarily complex, but is fully featured. Especially relative to Django's ORM.
 - SQLAlchemy is 100x easier if you understand what the resulting SQL looks like. Django lets you ease your way into that understanding.
 - The SQLAlchemy syntax is ugly. It's like SQL, but in Python, without concision. Meh.


## Example oddities of SQLAlchemy

### It's pedantic!

```python
jobs = Job.query.join(Person).filter(Person.name==name)
```

Why do I have to `.join(Person)` if I'm _also_ filtering by `Person.name==name`. I will _always_ want that join, so why don't you just do it for me. It's like saying "I'll have a ham sandwich with ham."

### It's got _barely_ masked SQL
```python
employers = db.session.query(Company.name, func.count(Company.id)) \
    .join(Job).join(Person) \
    .filter(Person.name==name).group_by(Company.name)
```

This is so wordy and complex (`func`?? Huh?) I may as well be writing raw SQL:

```sql
  SELECT c.name, count(1) cnt
    FROM companies c, jobs j, people p
   WHERE c.id = j.employer_id
     AND j.person_id = p.id
     AND p.name = :name_1
GROUP BY c.name
```

There's a legibility and flexibility cost to writing code in one language in another... but the simplicity of the resulting syntax is supposed to be greater than this cost. In this case, it's not worth it.

To see the benefit of SQLAlchemy in this case you have to recognize that not remembering _how_ each foreign key is mapped is a benefit. However, the relationships between the tables, and making sure to get them correctly expressed, is still crucial. The gains from SQLAlchemy's abstraction seem small.

### But it's sophisticated

```python
titles = db.session.query(Job.title).join(Person) \
    .filter(Person.name==name).distinct()
```

Using the session explicitly in the query is I suppose useful when you're working with transactions, or some place where you'd have multiple connections. Makes it super easy to have multiple databases, if you're into that kind of fanciness. Doesn't seem real-worldy that you'd want to write code _assuming_ you'll one day have multiple active database connections.

