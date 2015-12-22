from flask import request
from flask_admin import Admin
from flask_admin.base import expose
from flask_admin.contrib.sqla import ModelView

from app import create_app
from api import api, auth
from views import view

app = create_app()


class RecordAdmin(ModelView):
    form_excluded_columns = ('timestamp',)

    @expose('/new/', methods=('GET', 'POST'))
    # @auth.login_required
    def create_view(self):
        """
            Custom create view.
        """
        return super().create_view()


if __name__ == '__main__':
    app.register_blueprint(api)
    app.register_blueprint(view)

    from models import User, Record
    from app import db
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
        db.create_all()
    admin = Admin(app, name='api_admin', template_mode='bootstrap3')
    # admin.add_view(ModelView(User, db.session))
    admin.add_view(RecordAdmin(Record, db.session))
    app.run(debug=True, port=8000)
