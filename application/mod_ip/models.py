import datetime
from application.core import db


class Log(db.Model):
    """
    Log model
    """
    __tablename__ = 'log_table'

    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(15), nullable=False)
    user_agent = db.Column(db.String(120))
    datetime = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, ip_address, user_agent):
        self.ip_address = ip_address
        self.user_agent = user_agent

    def __repr__(self):
        return '<Log %r>' % self.ip_address
