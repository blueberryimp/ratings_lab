"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

    __tablename__ = "users"
    #inform SQLALchemy that instances of this class will be stored
    #in a table named users
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #add a column to the tabled named user_id cotaining integers and primary key
    email = db.Column(db.String(64), nullable=True)
    #add a column for email containing strings with optional null columns
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)


# Put your Movie and Rating model classes here.

class Movie(db.Model):
    """User of ratings website."""

    __tablename__ = "movies"
    #inform SQLALchemy that instances of this class will be stored
    #in a table named users
    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #add a column to the tabled named user_id cotaining integers and primary key
    title = db.Column(db.String(64), nullable=False)
    #add a column for email containing strings with optional null columns
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(256), nullable=True)

class Rating(db.Model):
    """User of ratings website."""

    __tablename__ = "ratings"
    #inform SQLALchemy that instances of this class will be stored
    #in a table named users
    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    #add a column to the tabled named user_id cotaining integers and primary key
    movie_id= db.Column(db.Integer, nullable=False)
    #add a column for email containing strings with optional null columns
    user_id = db.Column(db.Integer, nullable=False)
    score = db.Column(db.Integer, nullable=False)
##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
