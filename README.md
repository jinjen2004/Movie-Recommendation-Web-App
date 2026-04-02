Jenell Son


Movie Recommendation Website
   - This website allows users to browse movies, get recommendations, write reviews, and manage their reviews. It features user authentication, allowing users to create accounts, log in, and write reviews for movies. Users can also delete their own reviews. The application uses Flask as the back-end framework and Flask-SQLAlchemy for database management. The website is styled with HTML, CSS, and integrates user authentication features using Flask-Login.


- > Key Features
    User Authentication: Users can register, log in, and log out. Each user is linked to their reviews.
    Movie Reviews: Users can write reviews for movies, including a rating and content. Reviews are linked to both the user and the movie.
    Delete Reviews: Users can delete only their own reviews.
    Database: The application uses a relational database with two main tables: Movie and Review.
    Movie contains information such as title, genre, rating, and description.
    Review includes review content, a rating, and the associated movie and user.
    Dynamic Content: The movie list and reviews are dynamically pulled from the database and displayed on the website.


- > Database Structure
    The database contains two primary tables:

    Movie Table:
        id: Primary key.
        image_file: Filename for the movie image.
        title: The movie title.
        genre: Genre of the movie.
        rating: Rating of the movie.
        description: A brief description of the movie.

    Review Table:
        id: Primary key.
        content: Content of the review.
        rating: Rating given by the user.
        movie_id: Foreign key referencing the Movie table.
        user_id: Foreign key referencing the User table.
        created_at: Date and time the review was created.


- > Set up the database:
    Create the database by running the following commands in the Python shell:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            db.create_all()
        quit()

- > To run the code:
  > pip install -r requirements.txt
    python app.py

- > To populate the data (the movies doesn't show until you do this):
        http://127.0.0.1:5000/populate
