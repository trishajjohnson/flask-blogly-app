"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)



@app.route("/")
def show_homepage():
    """Shows homepage, welcome message and link to all users page"""

    return render_template("base.html")



@app.route("/users")
def list_all_users():
    """Lists all users, link to their details page and a 'Add User' button."""

    users = User.query.all()

    return render_template("all-users.html", users=users)



@app.route("/users/new")
def new_user_form():
    """Displays 'Create a User' form."""

    return render_template("add-user.html")



@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user and redirect to newly added user detail page."""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    image_url = request.form['image-url'] or None

    user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")



@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show detail on a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("detail.html", user=user)



@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    """Show edit page for selected user."""

    user = User.query.get_or_404(user_id)

    return render_template("edit-user.html", user=user)



@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Submits changes for selected user and rediercts to that user's detail page."""

    user = User.query.get_or_404(user_id)

        
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"] or None

    db.session.commit()

    return redirect("/users")



@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes selected user and rediercts to the users page."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

    