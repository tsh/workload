from flask import render_template, Blueprint

from models import Record

view = Blueprint('view', __name__, template_folder='../templates')


@view.route('/')
def hello_world():
    records = Record.query.all()
    import ipdb; ipdb.set_trace()
    return render_template('index.html', name='test', records=records)

