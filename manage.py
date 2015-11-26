"""
Script for start, shell, test of this project.
"""

# import system dependencies
import os

# import flask affixes
from flask.ext.script import Manager, Shell
from flask.ext.migrate import Migrate, MigrateCommand

# import other object from this project
from app import create_app, db
from app.models import User, Role, Conference, City, Topic


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)

def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role, Conference=Conference, \
            City=City, Topic=Topic)

manager.add_command("shell", Shell(make_context=make_shell_context))

@manager.command
def test():
    """
    Run unit tests of xing project
    """
    import unittest
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    # app.run(debug=True)
    manager.run()
