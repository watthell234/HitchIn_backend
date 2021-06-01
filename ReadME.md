# HitchIn Backend

1. `git clone this-repo`
2. `cd into-repo`
3. `pipenv shell`
4. `pipenv install` to install project dependencies.


## Database Migrations

Manage.py contains the migration scripts. In order to perform migrations after
model gets changed you must run the following commands

If first time running migration then run

`python`
`from models import db`
`db.create_all()`

1. `python manage.py db migrate`
2. `python manage.py db upgrade`
