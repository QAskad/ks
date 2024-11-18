from . import db
from flask_login import UserMixin

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

class Subgenre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('subgenres', lazy=True))

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    file_path = db.Column(db.String(300), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'), nullable=True)
    subgenre_id = db.Column(db.Integer, db.ForeignKey('subgenre.id'), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    genre = db.relationship('Genre', backref=db.backref('files', lazy=True))
    subgenre = db.relationship('Subgenre', backref=db.backref('files', lazy=True))
    user = db.relationship('User', backref=db.backref('uploaded_files', lazy=True))
