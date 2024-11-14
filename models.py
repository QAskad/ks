from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Genre(db.Model):
    __tablename__ = 'genres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Subgenre(db.Model):
    __tablename__ = 'subgenres'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'))

class File(db.Model):
    __tablename__ = 'files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(100))
    size = db.Column(db.Integer, nullable=False)
    download_count = db.Column(db.Integer, default=0)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.id'), nullable=True)
    subgenre_id = db.Column(db.Integer, db.ForeignKey('subgenres.id'), nullable=True)
    
    genre = db.relationship('Genre', backref=db.backref('files', lazy=True))
    subgenre = db.relationship('Subgenre', backref=db.backref('files', lazy=True))
