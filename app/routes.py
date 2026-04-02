from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db, bcrypt
from app.models import User
from app.forms import RegistrationForm, LoginForm, MovieForm, ReviewForm
from app.models import Movie, Review
from flask import abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint

main = Blueprint('main', __name__)

@main.route('/')
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies)

# Registration route
@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        login_user(user)
        return redirect(url_for('main.home'))

    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')

    return render_template('login.html', form=form)

# Logout route (requires authentication)
@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@main.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if query:
        movies = Movie.query.filter(Movie.title.like(f'%{query}%')).all()
    else:
        movies = Movie.query.all()
    return render_template('home.html', movies=movies)

@main.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    genres = db.session.query(Movie.genre).distinct()
    selected_genre = request.args.get('genre')

    if selected_genre:
        movies = Movie.query.filter_by(genre=selected_genre).all()
    else:
        movies = Movie.query.all()

    return render_template('recommendations.html', movies=movies, genres=genres, selected_genre=selected_genre)

@main.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    reviews = Review.query.filter_by(movie_id=movie.id).all()
    form = ReviewForm()
    return render_template('movie_details.html', movie=movie, reviews=reviews, form=form)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = ReviewForm()
    movies = Movie.query.all()
    reviews = Review.query.filter_by(user_id=current_user.id).all()
    form = ReviewForm()
    if form.validate_on_submit():
        movie = Movie.query.get(form.movie_id.data)
        if movie:
            review = Review(content=form.content.data, rating=form.rating.data, movie_id=movie.id, user_id=current_user.id)
            db.session.add(review)
            db.session.commit()
            flash('Your review has been added!', 'success')
            return redirect(url_for('main.dashboard'))

    return render_template('dashboard.html', form=form, movies=movies, reviews=reviews)

@main.route('/delete_review/<int:review_id>', methods=['POST'])
def delete_review(review_id):
    review = Review.query.get(review_id)
    if review and (review.user_id == current_user.id or current_user.is_admin):
        db.session.delete(review)
        db.session.commit()
        flash('Review deleted!', 'success')
    else:
        flash('You can only delete your own reviews.', 'danger')
    return redirect(url_for('main.dashboard'))

@main.route('/add_review/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def add_review(movie_id):
    return render_template('add_review.html', movie_id=movie_id)

@main.route('/populate')
def populate():
    populate_movies()
    return "Movies populated!"

def populate_movies():
    if Movie.query.count() == 0:
        movies = [
            Movie(image_file="inception.jpeg", title="Inception", genre="Sci-Fi", rating=8.8, description="A thief who steals corporate secrets through dream-sharing technology."),
            Movie(image_file="shawshank.jpeg", title="The Shawshank Redemption", genre="Drama", rating=9.3, description="Two imprisoned men bond over a number of years."),
            Movie(image_file="dark_knight.jpeg", title="The Dark Knight", genre="Action", rating=9.0, description="Batman faces the Joker, a criminal mastermind."),
            Movie(image_file="interstellar.jpeg", title="Interstellar", genre="Sci-Fi", rating=8.6, description="A team of explorers travel through a wormhole in space."),
            Movie(image_file="forrest.jpeg", title="Forrest Gump", genre="Drama/Romance", rating=8.8, description="The presidencies of Kennedy and Johnson, the Vietnam War, and more through the eyes of Forrest."),
            Movie(image_file="matrix.jpg", title="The Matrix", genre="Sci-Fi", rating=8.7, description="A computer hacker learns from mysterious rebels about the true nature of his reality."),
            Movie(image_file="pride.jpg", title="Pride and Prejudice (2005)", genre="Drama/Romance", rating=7.8, description="An adaptation of Jane Austen's novel about the emotional development of Elizabeth Bennet, the dynamic between her and Mr. Darcy, and family dynamics."),
            Movie(image_file="godfather.jpg", title="The Godfather", genre="Crime/Drama", rating=9.2, description="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son."),
            Movie(image_file="fight.jpg", title="Fight Club", genre="Drama", rating=8.8, description="An insomniac office worker forms an underground fight club with a soap salesman."),
            Movie(image_file="gladiator.png", title="Gladiator", genre="Action/Adventure", rating=8.5, description="A betrayed Roman general seeks revenge against the corrupt emperor who murdered his family and sent him into slavery."),
        ]
        db.session.add_all(movies)
        db.session.commit()
        print("Movies added!")
    else:
        print("Movies already exist.")