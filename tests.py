import os
import unittest

import api
from api import db, User


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = api.app.test_client()
        self.user = User(name='test')
        db.create_all()
        db.session.add(self.user)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_empty_db(self):
        resp = self.app.get('/users/')
        self.assertIn(self.user.get_url(), resp.data)

if __name__ == '__main__':
    api.app.config['TESTING'] = True
    os.environ['DATABASE_URL'] = 'sqlite:///test.sqlite'
    unittest.main()
