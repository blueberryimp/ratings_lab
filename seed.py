"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting
# this through the Flask-SQLAlchemy helper library. On this, we can
# find the `session` object, where we do most of our interactions
# (like committing, etc.)

db = SQLAlchemy()


#####################################################################
# Model definitions

class User(db.Model):
    """User of ratings website."""

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
    movie_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    score = db.Column(db.Integer)

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
seed.py
"""Utility file to seed ratings database from MovieLens data in seed_data/"""

import datetime
from sqlalchemy import func

from model import User, Rating, Movie, connect_to_db, db
from server import app


def load_users():
    """Load users from u.user into database."""

    print "Users"

    for i, row in enumerate(open("seed_data/u.user")):
        row = row.rstrip()
        user_id, age, gender, occupation, zipcode = row.split("|")

        user = User(age=age,
                    zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_movies():
    """Load movies from u.item into database."""

    print "Movies"

    for i, row in enumerate(open("seed_data/u.item")):
        row = row.rstrip()

        # clever -- we can unpack part of the row!
        movie_id, title, released_str, junk, imdb_url = row.split("|")[:5]

        # The date is in the file as daynum-month_abbreviation-year;
        # we need to convert it to an actual datetime object.

        if released_str:
            released_at = datetime.datetime.strptime(released_str, "%d-%b-%Y")
        else:
            released_at = None

        # Remove the (YEAR) from the end of the title.

        title = title[:-7]   # " (YEAR)" == 7

        movie = Movie(title=title,
                      released_at=released_at,
                      imdb_url=imdb_url)

        # We need to add to the session or it won't ever be stored
        db.session.add(movie)

        # provide some sense of progress
        if i % 100 == 0:
            print i

    # Once we're done, we should commit our work
    db.session.commit()


def load_ratings():
    """Load ratings from u.data into database."""

    print "Ratings"

    for i, row in enumerate(open("seed_data/u.data")):
        row = row.rstrip()

        user_id, movie_id, score, timestamp = row.split("\t")

        user_id = int(user_id)
        movie_id = int(movie_id)
        score = int(score)

        # We don't care about the timestamp, so we'll ignore this

        rating = Rating(user_id=user_id,
                        movie_id=movie_id,
                        score=score)

        # We need to add to the session or it won't ever be stored
        db.session.add(rating)

        # provide some sense of progress
        if i % 1000 == 0:
            print i

            # An optimization: if we commit after every add, the database
            # will do a lot of work committing each record. However, if we
            # wait until the end, on computers with smaller amounts of
            # memory, it might thrash around. By committing every 1,000th
            # add, we'll strike a good balance.

            db.session.commit()

    # Once we're done, we should commit our work
    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()
    load_movies()
    load_ratings()
    set_val_user_id()