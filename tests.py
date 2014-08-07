# -*- coding: utf-8 -*-
import os
from application.core import app
from application.core import db
from application.mod_ip.views import parse_ip
from application.mod_ip.models import Log
import unittest
import tempfile


class ProxyHack(object):
    """ Set REMOTE_ADDR in unittests """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ['REMOTE_ADDR'] = environ.get('REMOTE_ADDR', '127.0.0.1')
        return self.app(environ, start_response)


class CheckIpTestCase(unittest.TestCase):

    def setUp(self):
        """ Before each test, set up a blank database """
        self.db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        app.wsgi_app = ProxyHack(app.wsgi_app)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        """ Get rid of the database again after each test """
        os.close(self.db_fd)
        os.unlink(app.config['DATABASE'])

    def test_server_is_up_and_running(self):
        """ Test server """
        response = self.app.get('/')
        assert response._status_code == 200

    def test_404_page(self):
        """ Test 404 page """
        response = self.app.get('/qwerty')
        assert response._status_code == 404
        assert response.data == '404: Not Found'

    def test_xff(self):
        """ Test response data with XFF header """
        rv = self.app.get('/', headers={'X-Forwarded-For': '255.255.255.255'})
        assert '255.255.255.255' in rv.data

    def test_remote_addr(self):
        """ Test response data with no XFF header """
        rv = self.app.get('/')
        assert '127.0.0.1' in rv.data

    def test_log_add(self):
        """ Test Log model """
        log_record = Log(ip_address='123.123.123.123', user_agent='Mozilla/5.0')
        db.session().add(log_record)
        db.session().commit()

        assert log_record in db.session
        assert '123.123.123.123' == log_record.ip_address
        assert 'Mozilla/5.0' == log_record.user_agent

    def test_parse_ip(self):
        """ Test parse_ip method """
        assert '127.0.0.1' == parse_ip('127.0.0.1, 127.0.0.2')
        assert '99.99.99.99' == parse_ip('Proxy 99.99.99.99, 127.0.0.1')
        assert '0.0.0.0' == parse_ip('0.0.0.0')
        assert '123.123.123.123' == parse_ip('123.123.123.12345')
        assert '45.123.123.123' == parse_ip('12345.123.123.123')
        assert None == parse_ip('999.999.999.999')
        assert None == parse_ip('12345')
        assert None == parse_ip('1.2.256.3')


if __name__ == '__main__':
    unittest.main()
