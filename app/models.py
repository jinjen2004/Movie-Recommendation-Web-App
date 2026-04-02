from app import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    is_admin = db.Column(db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")

    @property
    def is_active(self):
        return True

    def __repr__(self):
        return f'<User {self.username}>'

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    genre = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    rating = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(100))

    reviews = db.relationship('Review', back_populates='movie', cascade="all, delete-orphan", lazy=True)

    def __repr__(self):
        return f"<Movie {self.title}>"

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    rating = db.Column(db.Integer, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='reviews')
    movie = db.relationship('Movie', back_populates='reviews')

    def __repr__(self):
        return f"Review('{self.content}', '{self.rating}', '{self.user.username}', '{self.created_at}')"
