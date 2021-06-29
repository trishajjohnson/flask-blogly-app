"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add sample users
user1 = User(first_name='Alan', last_name='Alda')
user2 = User(first_name='Joel', last_name='Burton')
user3 = User(first_name='Jane', last_name='Smith')

# Add new objects to session, so they'll persist
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)

# Commit--otherwise, this never gets saved!
db.session.commit()