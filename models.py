from datetime import datetime

from flask import url_for

from app import db
from utils import url_parse


class ValidationError(ValueError):
    pass


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    records = db.relationship('Record', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User: {}>".format(self.name)

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # TODO: add start, end date
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return "<Record: {}>".format(self.description[:50])

    def get_url(self):
        return url_for('api.get_records', id=self.id, _external=True)

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

