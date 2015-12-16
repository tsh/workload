from app import app
from api import api
from views import view



from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

if __name__ == '__main__':
    app.register_blueprint(api)
    app.register_blueprint(view)

    from models import User, Record
    from app import db

    admin = Admin(app, name='api_admin', template_mode='bootstrap3')
    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Record, db.session))
    app.run(debug=True, port=8000)
