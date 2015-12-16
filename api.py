from flask import jsonify, request, Blueprint

from app import app, db
from models import User, Record

api = Blueprint('api', __name__)


@api.route('/api/users/', methods=['GET'])
def get_users():
    return jsonify({'users': [user.get_url() for user in User.query.all()]})


@api.route('/api/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


@api.route('/api/users/', methods=['POST'])
def new_user():
    user = User()
    user.import_data(request.json)
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

