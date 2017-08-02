"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()

class User(db.Model):
    """User of ratings website."""
    #name of table called 'users'
    __tablename__ = "users" 

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s>" % (self.user_id,
                                               self.email)


class Movie(db.Model):
    """Movie on ratings website."""

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    title = db.Column(db.String(100))
    released_at = db.Column(db.DateTime)
    imdb_url = db.Column(db.String(200))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Movie movie_id=%s title=%s>" % (self.movie_id,
                                                 self.title)


class Rating(db.Model):
    """Rating of a movie by a user."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)

    #this is defining the foreign key as movies.movie_id
    # it references another column in another table (parent table)
    movie_id = db.Column(db.Integer,
                         db.ForeignKey('movies.movie_id'))

    # this is defining the foreign key as users.user_id
    # the user_id column of the ratings table refers to the user_id column of 
    # the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    score = db.Column(db.Integer)


    # Define relationship to user
    #establishes the relationship between Rating and User objects
    # backref means the relationship between User and rating is both ways
    #listener on both sides which will mirror atrribute operations on both directions
    #when we type r = Rating.query.get(1)...we can print r.user_id
    user = db.relationship("User",
                           backref=db.backref("ratings",
                                              order_by=rating_id))

    # Define relationship to movie
    movie = db.relationship("Movie",
                            backref=db.backref("ratings",
                                               order_by=rating_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Rating rating_id=%s movie_id=%s user_id=%s score=%s>"
        return s % (self.rating_id, self.movie_id, self.user_id,
                    self.score)


#####################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///ratings'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
