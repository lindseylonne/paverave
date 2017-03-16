"""Models and database functions for paverave project."""
# import heapq
# import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
# from sqlalchemy import Table, Column, Integer, ForeignKey

#  Do i need both of these?
# from SQLAlchemy import DateTime
import datetime

# import correlation

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of PaveRave site."""

    __tablename__ = "users"

    # TODO: start ids at high number?
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    # TODO: add email format check and account verification with email link
    email = db.Column(db.String(64), unique=True, nullable=False)
    # TODO: secure pwd and add min requirements
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    date_modified = db.Column(db.DateTime)
    date_removed = db.Column(db.DateTime)
    profile_url = db.Column(db.String(255))
    profile_picture_url = db.Column(db.String(255))

    # Define relationship to Vehicle db through UserVehicle
    vehicles = relationship("UserVehicle", back_populates="user")

        # Define relationship to user db through UserVehicles
    comments = relationship("CommentUpvote", back_populates="user")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s email=%s username = %s>" % (self.user_id, self.email, self.username)


class UserVehicle(db.Model):  # do we need this once users claim vehicles? Or just add to owner field in vehicle table?
    """Association table for users and vehicles on paverave site because vehicles can exist without user."""

    __tablename__ = "uservehicles"

    # Q: do we need id for association table?
    # A: (yes, there can be multiple usrs per vehicle, and multiple vehicles per user.)
    user_vehicle_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    vehicle_plate = db.Column(db.String(64), db.ForeignKey('vehicles.vehicle_plate'))
    date_linked = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    date_unlinked = db.Column(db.DateTime)

    # from Association object secion here: http://docs.sqlalchemy.org/en/latest/orm/basic_relationships.html
    vehicle = relationship("Vehicle", back_populates="users")
    user = relationship("User", back_populates="vehicles")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<UserVehicle user_vehicle_id=%d user_id=%d vehicle_plate=%d>" % (self.user_vehicle_id, self.user_id, self.vehicle_plate)


class Vehicle(db.Model):
    """Vehicle on PaveRave site."""

    __tablename__ = "vehicles"

    # TODO: Beta version, allow users to add more vehicle info, incl pics
    vehicle_plate = db.Column(db.String(64), primary_key=True)  # license plate
    # TODO: Beta version, add region and country plate formats including symbols.
    vtype = db.Column(db.String(64))  # car, truck, motorcycle, semi, plane, boat, etc.
    vstyle = db.Column(db.String(64))  # sedan, coupe, flatbed, hazmat, sport, etc.
    make = db.Column(db.String(64))
    model = db.Column(db.String(64))
    color = db.Column(db.String(64))
    user_id_adder = db.Column(db.Integer, nullable=False)  # user adding car
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    # TODO: move owner to UserVehicles association table?
    user_id_owner = db.Column(db.Integer)
    vpic_url = db.Column(db.String(255))  # TODO: beta, add ability to add vehicle photo url

    # Define relationship to user db through UserVehicles
    users = relationship("UserVehicle", back_populates="vehicle")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Vehicle vehicle_plate=%d>" % (self.vehicle_plate)


class Post(db.Model):
    """Post on PaveRave site by a user about vehicle."""

    __tablename__ = "posts"

    post_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    vehicle_plate = db.Column(db.String(64), db.ForeignKey('vehicles.vehicle_plate'))
    event_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    ptype = db.Column(db.String(64), nullable=False)
    location = db.Column(db.String(255))
    latitude = db.Column(db.Numeric(precision=9, scale=6))
    longitude = db.Column(db.Numeric(precision=9, scale=6))
    topic = db.Column(db.String(255), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    date_modified = db.Column(db.DateTime)
    date_removed = db.Column(db.DateTime)
    comment_count = db.Column(db.Integer, default=0)

    # Define relationship to users db
    user = db.relationship("User", backref=db.backref("paverave", order_by=user_id))

    # Define relationship to vehicles db
    vehicle = db.relationship("Vehicle", backref=db.backref("paverave", order_by=vehicle_plate))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Roadrate post_id=%s user_id=%s vehicle_plate=%s event_date=%s ptype=%s latitude=%s longitude=%s topic=%s>" % (
            self.post_id, self.user_id, self.vehicle_plate, self.event_date, self.ptype, self.latitude, self.longitude, self.topic)


class Comment(db.Model):
    """Comments on a post on PaveRave site."""

    # TODO: crate commentPings association table to enable user pings in jquery-comments

    __tablename__ = "comments"

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.post_id'))
    cid = db.Column(db.String(64), nullable=False)  # used by jquery-comments for position in thread
    parent = db.Column(db.String(64), default="null", nullable=False)  # null means first comment in thread for jquery-comments
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
    date_modified = db.Column(db.DateTime)
    # Either content or fileURL must be present for jquery_comments
    content = db.Column(db.String(255), nullable=False)
    file_url = db.Column(db.String(255))
    pings = db.Column(db.String(255))
    upvotes = db.Column(db.Integer, default=0, nullable=False)
    date_removed = db.Column(db.DateTime)

    # Define relationship to posts db
    post = db.relationship("Post", backref=db.backref("paverave", order_by=post_id))

    # Define relationship to user db through UserVehicles
    users = relationship("CommentUpvote", back_populates="comment")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Roadrate comment_id=%d user_id=%d post_id=%d cid=%s parent=%s date_created=%s date_modified=%s content=%s upvotes=%d>" % (
            self.comment_id, self.user_id, self.post_id, self.cid, self.parent, self.date_created, self.content, self.upvotes)


class CommentUpvote(db.Model):
    """Upvotes on a comment on a post on the PaveRave site."""

    __tablename__ = "commentupvotes"
    upvote_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.comment_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

    # # Define relationship to comments table
    # comment = db.relationship("Comment", backref=db.backref("paverave", order_by=comment_id))

    # # Define relationship to users table
    # user = db.relationship("User", backref=db.backref("paverave", order_by=user_id))

    comment = relationship("Comment", back_populates="users")
    user = relationship("User", back_populates="comments")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Roadrate upvote_id=%d comment_id=%s user_id=%d>" % (
            self.upvote_id, self.comment_id, self.user_id)


##############################################################################
# Helper functions

# def connect_to_db(app):
#     """Connect the database to our Flask app."""

#     # Configure to use our PostgreSQL database
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///paverave'

def connect_to_db(app, db_uri=None):
    """Connect our application to our database."""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgres:///paverave'

#    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
