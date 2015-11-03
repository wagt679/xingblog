# import system dependencies
import os

# import flask affixes
from flask.ext.script import Manager, Shell

# import other object from this project
from app import create_app


# create the app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

# run the app
if __name__ == "__main__":
    app.run(debug=True)
