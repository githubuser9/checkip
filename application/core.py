# Import flask and template operator
from flask import Flask, render_template

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported by modules and controllers
db = SQLAlchemy(app)


@app.errorhandler(404)
def not_found(error):
    """
    Http errors handler
    :param error: Error message
    :return: render_template object
    """
    return render_template('error.html', error_message=error), 404


from application.mod_ip.views import mod_ip

app.register_blueprint(mod_ip)

# Build the database
db.create_all()

