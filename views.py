from flask import render_template, Blueprint

from models import Record

view = Blueprint('view', __name__, template_folder='../templates')


@view.route('/')
def index():
    records = Record.query.all()
    return render_template('index.html', name='test', records=records)

