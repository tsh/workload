import os

from datetime import datetime
from dateutil import parser as datetime_parser
from dateutil.tz import tzutc
from flask import Flask, url_for, jsonify, request
from flask.ext.sqlalchemy import SQLAlchemy

from .utils import url_parse

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, '../data.sqlite')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_path

db = SQLAlchemy(app)


class ValidationError(ValueError):
    pass


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    records = db.relationship('Record', backref='users', lazy='dynamic')

    def get_url(self):
        return url_for('get_user', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'name': self.name,
            'records_url': url_for('get_user_records', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.name = data['name']
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        return self


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # TODO: add start, end date
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def get_url(self):
        return url_for('get_record', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'description': self.description
        }

    def import_data(self, data):
        try:
            self.description = self.data['description']
        except KeyError as e:
            raise ValidationError('Invalid record: ' + e.args[0])
        return self
    

@app.route('/users/', methods=['GET'])
def get_users():
    return jsonify({'users': [user.get_url() for user in User.query.all()]})


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).export_data())


@app.route('/users/', methods=['POST'])
def new_user():
    user = User()
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({}), 201, {'Location': user.get_url()}


@app.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    user = User.query.get_or_404(id)
    user.import_data(request.json)
    db.session.add(user)
    db.session.commit()
    return jsonify({})


@app.route('/users/<int:id>/records/', methods=['GET'])
def get_user_records(id):
    user = User.query.get_or_404(id)
    return jsonify({'records': [record.get_url() for record in user.records.all()]})


@app.route('/users/<int:id>/records/', methods=['POST'])
def new_record(id):
    user = User.query.get_or_404(id)
    record = Record(user=user)
    record.import_data(request.json)
    db.session.add(record)
    db.session.commit()
    return jsonify({}), 201, {'Location': record.get_url()}


@app.route('/records/', methods=['GET'])
def get_records():
    return jsonify({'records': [record.export_data() for record in Record.query.all()]})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
