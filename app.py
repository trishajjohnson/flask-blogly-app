"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

@app.route("/")
def show_homepage():
    """Shows homepage, welcome message and link to all users page"""

    return render_template("base.html")

@app.route("/all-users")
def list_all_users():
    """Lists all users, link to their details page and a 'Add User' button."""

    users = User.query.all()

    return render_template("all_users.html", users=users)

@app.route("/add-user")
def list_users():
    """Displays 'Add User' form."""

    return render_template("add_user.html")

@app.route("/add-user", methods=["POST"])
def add_user():
    """Add user and redirect to newly added user detail page."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/{user.id}")

@app.route("/<int:user_id>")
def show_pet(user_id):
    """Show info on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)

    