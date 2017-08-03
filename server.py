"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')#route to homepage
def index():
    """Homepage."""
    return render_template("homepage.html")#return homepage

@app.route("/users")
def user_list():
    """Show list of users."""
    users = User.query.all()#query all user data from User class
    return render_template('user_list.html', users=users)#return users.html


#gets request to get user information for registration
@app.route('/register', methods=['GET'])
def register():
    return render_template('register_form.html')#gets form info from register_form

#post for receive(post) what information we have gotten
@app.route('/register', methods=['POST'])
def register_process():
    """Process registration information."""
    #create a variable called user and receive all of the information we
    #requested from our registration form
    email = request.form['email']#gets email from register_form.html
    password=request.form['password']#gets password from register_form.html
    age=request.form['age']#gets age from register_form.html
    zipcode=request.form['zipcode']#gets zipcode from register_form.html

    #enters in the information we collected and assigns it to the variable 'user'
    user = User(email=email, password=password, age=age, zipcode=zipcode)
    db.session.add(user)#add user to the User database
    db.session.commit()#commit our add to the User database
    flash('User successfully registered!')#flash message that shows user is 
    #successfull registered
    return redirect('/users')
    #route redirects back to users ('/users')


#return the login_form.html template using get method to get information
@app.route('/login', methods=['GET'])
def login_form():
    """Render login form."""
    return render_template("login_form.html")#return login_form.html

#receive information we got from login_form.html with post method
@app.route('/login', methods=['POST'])
def login_process():
    """Process login information."""
    email = request.form["email"]#get 'email' variable from login_form.html
    password = request.form["password"]#get 'password' variable from login_form.html

    #get user query from User database db.model on model.py
    user = User.query.filter_by(email=email).first()


    if user == None:#if email does not exist in our query search above
        flash("User does not exist!")
        return redirect("/login")#return to login_form.html so the user can re-enter info

    if user.password != password:
        flash("You have entered the wrong password!")
        return redirect("/login")#return to login_form.html so the user can re-enter pw

    session["user_id"] = user.user_id#add user_id to session dictionary

    flash("Logged in")#flash a message that says "Logged in"
    return redirect("/users")#redirect to user_list.html


# @app.route('/logout')
# def logout():
#     """Log out page."""
#     del session["user_id"]#del user from the session
#     flash("Logged Out.")
#     return redirect("/")#redirect back to homepage


# @app.route("/users/<int:user_id>")
# def user_detail(user_id):
#     """Show info about user."""
#     user = User.query.get(user_id)#
#     return render_template("users.html", user=user)


# @app.route("/movies")
# def movie_list():
#     """Show list of movies."""

#     movies = Movie.query.order_by('title').all()
#     return render_template("movie_list.html", movies=movies)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    app.run(port=5000, host='0.0.0.0')
