import os
import tempfile
import unittest

from app import create_app, db
import api, views
import models
app = create_app()


class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.test_db_file = tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.test_db_file
        app.testing = True
        self.app = app.test_client()

        self.user = models.User(username='test')
        with app.app_context():
            db.create_all()
            db.session.add(self.user)
            db.session.commit()

    def tearDown(self):
        os.remove(self.test_db_file)
        # db.session.remove()
        # db.drop_all()

    def test_users(self):
        with app.test_client() as c:
            resp = c.get('/api/users/')
        assert resp.status_code == 200

if __name__ == '__main__':
    # TODO: register blueprints in same place as with run.py
    app.register_blueprint(api.api)
    app.register_blueprint(views.view)
#     api.app.config['TESTING'] = True
#     os.environ['DATABASE_URL'] = 'sqlite:///test.sqlite'
    unittest.main()
