import argparse

from flask import request
from flask_admin import Admin
from flask_admin.base import expose
from flask_admin.contrib.sqla import ModelView

from app import create_app, db
from api import api, auth
from models import User
from views import view

app = create_app()


class RecordAdmin(ModelView):
    form_excluded_columns = ('timestamp',)

    @expose('/new/', methods=('GET', 'POST'))
    @auth.login_required
    def create_view(self):
        """
            Custom create view.
        """
        return super().create_view()


def create_user(username, password):
        if username is None or password is None:
            print('Please provied username:password')
            raise Exception
        with app.app_context():
            if User.query.filter_by(username=username).first() is not None:
                print('This user is already exists')
                raise Exception
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--add_user", help="create user with  username:password")
    args = parser.parse_args()
    if args.add_user:
        username, password = args.add_user.split(':')
        create_user(username, password)
    else:
        app.register_blueprint(api)
        app.register_blueprint(view)

        from models import User, Record
        from app import db
        with app.app_context():
            db.create_all()
        admin = Admin(app, name='api_admin', template_mode='bootstrap3')
        admin.add_view(ModelView(User, db.session))
        admin.add_view(RecordAdmin(Record, db.session))
        app.run(debug=True, port=8000)
