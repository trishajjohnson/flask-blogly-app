"""Blogly application."""

from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post

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

    users = User.query.order_by(User.last_name, User.first_name).all()

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

    return redirect(f"/users/{ user.id }")



@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """Show detail on a single user."""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.id)

    return render_template("detail.html", user=user, posts=posts)



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


    
@app.route("/users/<int:user_id>/posts/new")
def show_new_post_form(user_id):
    """Displays new post form."""

    user = User.query.get_or_404(user_id)

    return render_template("new-post.html", user=user)



@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Adds new post to the DB and redirects back to user detail page."""

    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{ user_id }")



@app.route("/users/<int:user_id>/posts/<int:post_id>")
def show_post_detail(user_id, post_id):
    """Displays individual post detail page."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    return render_template('post-detail.html', user=user, post=post)



@app.route("/users/<int:user_id>/posts/<int:post_id>/edit")
def edit_post_form(user_id, post_id):
    """Displays edit post page."""

    user = User.query.get_or_404(user_id)
    post = Post.query.get_or_404(post_id)

    return render_template('edit-post.html', user=user, post=post)



@app.route("/users/<int:user_id>/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(user_id, post_id):
    """Submits changes to post and redirects to post detail page."""

    post = Post.query.get_or_404(post_id)

    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f'/users/{ user_id }/posts/{ post_id }')



@app.route("/users/<int:user_id>/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(user_id, post_id):
    """Deletes selected post and redirects to the users detail page."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{ user_id }")
