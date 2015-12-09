from flask import render_template, Blueprint

view = Blueprint('view', __name__, template_folder='../templates')


@view.route('/')
def hello_world():
    return render_template('index.html', name='test')

