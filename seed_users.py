"""Seed file to make sample data for users db."""

from models import User, Post, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
# User.query.delete()

# Add sample users
user1 = User(first_name='Alan', last_name='Alda')
user2 = User(first_name='Joel', last_name='Burton')
user3 = User(first_name='Jane', last_name='Smith')

# Add sample posts
post1 = Post(title="My first post", content="I don't really know what to say in this post.  So I'll just say hi.", user_id=1)
post2 = Post(title="I guess this is my 2nd post", content="Another day.  Another dollar. The end.", user_id=1)
post3 = Post(title="Post #3", content="What can I say?  This is a fake post!", user_id=1)
post4 = Post(title="This is a post from someone else", content="So we can test that not all posts are being posted in the loop!", user_id=2)

# Add sample tags 
tag1 = Tag("Fun")
tag2 = Tag("The Great Outdoors")
tag3 = Tag("Adventure")
tag4 = Tag("Live Music")

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)

db.session.add(tag1)
db.session.add(tag2)
db.session.add(tag3)
db.session.add(tag4)

# Commit--otherwise, this never gets saved!
db.session.commit()