from flask import jsonify, request, Blueprint, abort, g
import itsdangerous

from app import db
from models import User, Record
from flask.ext.httpauth import HTTPBasicAuth

api = Blueprint('api', __name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username_or_token, password=None):
    # first try to authenticate by token
    try:
        user = User.verify_auth_token(username_or_token)
    except itsdangerous.BadSignature:
        # try to authenticate with username/password
        user = User.query.filter_by(username=username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@api.route('/api/token/')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token})


@api.route('/api/users/', methods=['GET'])
def get_users():
    return jsonify({'users': [user.get_url() for user in User.query.all()]})


@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


@api.route('/api/users/', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)  # missing arguments
    if User.query.filter_by(username=username).first() is not None:
        abort(400)  # existing user
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return jsonify({}), 201, {'Location': user.get_url()}


@api.route('/api/users/<int:id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({})


@api.route('/api/users/<int:id>/records/', methods=['GET'])
def get_user_records(id):
    user = User.query.get_or_404(id)
    return jsonify({'records': [record.get_url() for record in user.records.all()]})


@api.route('/api/users/<int:id>/records/', methods=['POST'])
def new_record(id):
    user = User.query.get_or_404(id)
    record = Record(user=user)
    record.import_data(request.json)
    db.session.add(record)
    db.session.commit()
    return jsonify({}), 201, {'Location': record.get_url()}


@api.route('/api/records/', methods=['GET'])
def get_records():
    return jsonify({'records': [record.export_data() for record in Record.query.all()]})

