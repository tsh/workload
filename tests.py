import os
import api
import unittest
import tempfile

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
        api.app.config['TESTING'] = True
        self.app = api.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(api.app.config['DATABASE'])

    def test_empty_db(self):
        resp = self.app.get('/users/')
        assert False

if __name__ == '__main__':
    api.app.config['TESTING'] = True
    unittest.main()
