import os
import api
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, api.app.config['DATABASE'] = tempfile.mkstemp()
        api.app.config['TESTING'] = True
        self.app = api.app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(api.app.config['DATABASE'])

    def test_empty_db(self):
        rv = self.app.get('/users/')
        assert 'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()
