# from flask import Flask
# from views.views import view
#
# app = Flask(__name__)
# app.register_blueprint(view)


from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

if __name__ == '__main__':
    from app import app
    from api import api
    app.register_blueprint(api)

    from models import User, Record
    from app import db

    admin = Admin(app, name='api_admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Record, db.session))
    app.run(debug=True, port=8000)
