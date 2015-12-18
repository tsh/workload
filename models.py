from datetime import datetime

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from app import db, create_app
app = create_app()


class ValidationError(ValueError):
    pass


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    records = db.relationship('Record', backref='user', lazy='dynamic')
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User: {}>".format(self.username)

    # AUTH & REGISTRATION

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expires_in=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expires_in)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        data = s.loads(token)
        return User.query.get(data['id'])

    # OTHER

    def get_url(self):
        return url_for('api.get_user', id=self.id, _external=True)

    def export_data(self):
        return {
            'self_url': self.get_url(),
            'username': self.username,
            'records_url': url_for('get_user_records', id=self.id, _external=True)
        }

    def import_data(self, data):
        try:
            self.username = data['username']
        except KeyError as e:
            raise ValidationError('Invalid user: missing ' + e.args[0])
        return self


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    started = db.Column(db.DateTime)
    finished = db.Column(db.DateTime)
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

