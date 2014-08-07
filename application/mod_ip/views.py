# Import flask dependencies
from flask import Blueprint
from flask import render_template
from flask import request

# Import the database object from the main module
from application.core import db

# Import Log model
from models import Log

# Define the blueprint
mod_ip = Blueprint('ip', __name__, url_prefix='/')


def parse_ip(ip):
    """
    Search any valid IP with regexp and return first IP value if matched
    :param ip: possible string with IP address
    :return: IP address or None
    """

    import re

    search_ip = re.search('(?:(?:2[0-4]\d|25[0-5]|1\d{2}|[1-9]?\d)\.){3}(?:2[0-4]\d|25[0-5]|1\d{2}|[1-9]?\d)', ip)

    if search_ip:
        return search_ip.group(0)


@mod_ip.route('/', methods=['GET', ])
def index():
    """
    Main view
    :return: render_template object
    """

    current_ip = request.environ.get('REMOTE_ADDR')  # Client remote IP address

    xff = request.headers.getlist("X-Forwarded-For")  # Client X-Forwarded-For http header

    ua = request.environ.get('HTTP_USER_AGENT')  # Client User-Agent http header

    if xff:
        '''
        X-Forwarded-For header can be easily spoofed, so we need validate it.
        Set current IP as XFF if it's legit or leave remote IP otherwise.
        '''
        ip = parse_ip(xff[0])
        if ip is not None:
            current_ip = ip

    # Insert to database
    log_record = Log(ip_address=current_ip, user_agent=ua)
    db.session().add(log_record)
    db.session().commit()

    return render_template('index.html', ip=current_ip)

