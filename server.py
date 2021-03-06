"""paverave site allows users to post comments to vehicle license plates."""

from passlib.hash import argon2
from jinja2 import StrictUndefined
from flask import Flask, render_template, request, flash, redirect, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from model import connect_to_db, db, User, Post, Vehicle, Comment
# from pygeocoder import Geocoder
import json

# for heroku
import os
# import psycopg2
# import urlparse

# from sqlalchemy.sql import and_
# from sqlalchemy import Date, cast
# from datetime import date, datetime

# TODO: ? install pycipher 0.5.2


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
# app.secret_key = "ABC"
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

# Create instance of argon2 password hasher
# ph = PasswordHasher()

# TODO: refactor code to fewer routes (index, posts, map, profile, login/register) and AJAX calls for the rest.


@app.route('/')
def index():
    """Homepage."""

    return render_template("index.html")


@app.route('/register', methods=['GET'])
def register_form():
    """Show form for user signup."""

    # TODO: check if user logged in, redirect to profile. flash message

    return render_template("user_register.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process registration."""

    # Get form variables
    email = request.form["email"]
    username = request.form["username"]
    passwd = request.form["password"]

    if not email:
        flash("Missing email. Please try again.")
        return redirect("/register")

    if not passwd:
        flash("Missing password. Please try again.")
        return redirect("/register")

    if not username:
        flash("Missing username. Please try again.")
        return redirect("/register")

    # hashed = ph.hash(passwd)
    hashed = argon2.hash(passwd)
    del passwd

    # TODO: check fields and db without reloading page. Ajax. Keep filled fields.
    # TODO: if user exists, offer forgot password, pwd hint, etc.
    existing_uname = User.query.filter_by(username=username).first()
    if existing_uname:
        flash("Username already exists. Please try again.")
        return redirect("/register")

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        flash("Email already exists. Please try again.")
        return redirect("/register")

    # Add the new user to the database
    new_user = User(email=email, password=hashed, username=username)
    db.session.add(new_user)
    db.session.commit()

    # get the newly added user's generated user_id from the database to set session cookie
    user = User.query.filter_by(email=email, password=hashed).first()

    # set session cookie for newly added user
    session['user_id'] = user.user_id
    flash("User %s added." % email)

    return redirect("/profile/%s" % user.user_id)


@app.route('/login', methods=['GET'])
def login_form():
    """Show login form."""

    return render_template("user_login.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process login."""

    # Get form variables
    email = request.form["email"]
    passwd = request.form["password"]

    if not email:
        flash("Missing email. Please try again.")
        return redirect("/login")

    if not passwd:
        flash("Missing password. Please try again.")
        return redirect("/login")

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("No user found with that email. Please try again.")
        return redirect("/login")
    else:
        # hashed = argon2.hash(passwd)
        # del passwd
        if (argon2.verify(passwd, user.password)):
            session["user_id"] = user.user_id
            # TODO: add username or email to flash message.
            flash("Logged in successfully.")
            return redirect("/profile/%s" % user.user_id)
        else:
            flash("Password does not match.")
            return redirect("/login")


@app.route('/logout')
def logout():
    """Log out."""

    # if (session["user_id"]):
    if ("user_id" in session):
        del session["user_id"]
    flash("Logged Out.")
    return redirect("/login")


@app.route("/profile/<int:user_id>", methods=['GET'])
def show_user_detail(user_id):
    """Show info about user."""

    # user_id = session.get("user_id")

    # TODO: add security to redirct to login if no user session
    # TODO: check for userid and add to return if exists
    user = User.query.get(user_id)
    return render_template("user_profile.html", email=user.email, username=user.username)


@app.route("/profile/edit/<int:user_id>", methods=['GET'])
def show_user_profile_for_edit(user_id):
    """Show info about user for editing."""

    # user_id = session.get("user_id")
    # TODO: add security to redirct to login if no user session
    # TODO: check for userid and add to return if exists
    user = User.query.get(user_id)

    return render_template("user_profile_edit.html", email=user.email, username=user.username)


@app.route("/profile/edit/<int:user_id>", methods=['POST'])
def edit_user_detail(user_id):
    """Edit info about user."""

    # user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to access posts.")
        return redirect("/login")
        # raise Exception("No user logged in.")

    # Get form variables
    email = request.form["email"]
    # old_pwd = request.form["old_pwd"]
    username = request.form["username"]
    new_pwd = request.form["new_pwd"]

    user = User.query.get(user_id)
    # TODO: iterate through form variables to eliminate blanks
    # TODO: make sure old_pwd matches one in DB
    # TODO: secure pwds
    # TODO: only change variables that have changed
    # if (user.password == old_pwd):

    if user:
        user.email = email
        if (new_pwd):
            user.password = new_pwd
        user.username = username
        flash("Profile updated.")
    else:
        flash("Error updating profile.")
        return redirect("/profile/edit/%s" % user_id)

    # else:
    #     flash("Current password doesnt match. Try again.")
    #     return redirect("/profile/edit/%s" % user_id)

    db.session.commit()

    return redirect("/profile/%s" % user_id)


@app.route("/posts/map", methods=['GET'])
def posts_map():
    """Show map of post locations."""

    posts = Post.query.order_by(Post.event_date.desc()).limit(100).all()

    for post in posts:
        post.event_date = post.event_date.strftime('%m/%d/%Y %I:%M %P')

        # user = User.query.filter_by(user_id=post.user_id).first()
        # post.username = user.username
    # TODO: add username to posts db so we do not double query?

    api_key = os.environ['GOOGLE_MAPS_API_KEY']

    return render_template("post_map.html", posts=posts, api_key=api_key)


@app.route('/post_locations.json')
def post_location_info():
    """JSON information about post locations for map."""

    locations = {}
    counter = 0
    posts = Post.query.order_by(Post.event_date.desc()).limit(100).all()

    for post in posts:
        latitude = str(post.latitude)
        longitude = str(post.longitude)
        if (latitude != "None") and (longitude != "None"):
            locations[counter] = {'latitude': latitude, 'longitude': longitude, 'vehicle_plate': post.vehicle_plate, 'topic': post.topic}
            counter = counter + 1

    # print locations
    return jsonify(locations)


@app.route("/posts", methods=['GET'])
def posts_list():
    """Show list of all posts for all users."""

    posts = Post.query.order_by(Post.event_date.desc()).limit(100).all()
    for post in posts:
        post.event_date = post.event_date.strftime('%m/%d/%Y %I:%M %P')
        user = User.query.filter_by(user_id=post.user_id).first()
        post.username = user.username
    # TODO: add username to posts db so we do not double query?

    return render_template("post_list.html", posts=posts)


@app.route("/posts/<int:user_id>", methods=['GET'])
def user_posts_list(user_id):
    """Show list of all posts by specified user."""

    # user_id = session.get("user_id")

    # if user_id:
    posts = Post.query.filter_by(user_id=user_id).order_by(Post.event_date.desc()).limit(100).all()
    for post in posts:
        post.event_date = post.event_date.strftime('%m/%d/%Y %I:%M %P')
        user = User.query.filter_by(user_id=post.user_id).first()
        post.username = user.username
    # else:
    #     flash("Please log in to access posts.")
    #     return redirect("/login")

    return render_template("post_list.html", posts=posts)


@app.route("/posts/user/<int:user_id>", methods=['GET'])
def user_posts_list_session(user_id):
    """Show list of all posts by specified user if logged in."""

    user_id = session.get("user_id")

    if user_id:
        posts = Post.query.filter_by(user_id=user_id).order_by(Post.event_date.desc()).limit(100).all()
        for post in posts:
            post.event_date = post.event_date.strftime('%m/%d/%Y %I:%M %P')
            user = User.query.filter_by(user_id=post.user_id).first()
            post.username = user.username
    else:
        flash("Please log in to access posts.")
        return redirect("/login")

    # TODO: add script to posts_list page to highlight correct nav menu and eliminate this page.
    return render_template("user_posts.html", posts=posts)


@app.route("/post_comments.json", methods=['GET'])
def post_detail_comments_json():
    """Show details about a post including comments."""

# TODO: enable upvoting in jquery_comments and modify db model to handle userHasUpvoted data
# set these vars for jquery_comments...

    user_id = session.get("user_id")
    post_id = int(request.args.get("post_id"))

    if user_id:
        # get post data
        user_post = Post.query.filter_by(post_id=post_id).first()
        user_post.event_date = user_post.event_date.strftime('%m/%d/%Y %I:%M %P')
        user = User.query.filter_by(user_id=user_post.user_id).first()
        user_post.username = user.username
        # get comments
        post_comments = Comment.query.filter_by(post_id=post_id).limit(100).all()
        for comment in post_comments:
            # comment.date_created = comment.date_created.strftime('%Y-%m-%d')
            comment.date_created = comment.date_created.strftime('%Y, %m, %d %H:%M:%S')
            # comment.date_created = comment.date_created.strftime('%Y-%m-%dT%H:%M:%f+00:00')
            if (comment.date_modified):
                # comment.date_modified = comment.date_modified.strftime('%Y-%m-%d')
                # comment.date_modified = comment.date_modified.strftime('%Y-%m-%dT%H:%M:%f+00:00')
                comment.date_modified = comment.date_modified.strftime('%Y, %m, %d %H:%M:%S')
            if (user_id == comment.user_id):
                comment.created_by_current_user = True
            else:
                comment.created_by_current_user = False
            # remove from beginnso can be converted to json
            del comment._sa_instance_state
    else:
        flash("Please log in to access posts.")
        return redirect("/login")

    # convert to dictionary format
    post_comments = [comment.__dict__ for comment in post_comments]

    # convert to json format
    post_comments = json.dumps(post_comments)

    return jsonify({'comments': post_comments})


@app.route("/posts/detail/comments/<int:post_id>", methods=['GET'])
def post_detail_comments(post_id):
    """Show details about a post including comments."""

# TODO: enable upvoting in jquery_comments and modify db model to handle userHasUpvoted data
# set these vars for jquery_comments...

    user_id = session.get("user_id")

    # if user_id:
        # get post data
    user_post = Post.query.filter_by(post_id=post_id).first()
    user_post.event_date = user_post.event_date.strftime('%m/%d/%Y %I:%M %P')
    user = User.query.filter_by(user_id=user_post.user_id).first()
    user_post.username = user.username
    # get comments
    post_comments = Comment.query.filter_by(post_id=post_id).limit(100).all()
    for comment in post_comments:
        # comment.date_created = comment.date_created.strftime('%Y-%m-%d')
        comment.date_created = comment.date_created.strftime('%Y-%m-%dT%H:%M:%f+00:00')
        if (comment.date_modified):
            # comment.date_modified = comment.date_modified.strftime('%Y-%m-%d')
            comment.date_modified = comment.date_modified.strftime('%Y-%m-%dT%H:%M:%f+00:00')
        if (user_id == comment.user_id):
            comment.created_by_current_user = True
        else:
            comment.created_by_current_user = False
        # remove from beginnso can be converted to json
        del comment._sa_instance_state
    # else:
    #     flash("Please log in to access posts.")
    #     return redirect("/login")

    # convert to dictionary format
    post_comments = [comment.__dict__ for comment in post_comments]
    # print post_comments
    # convert to json format
    post_comments = json.dumps(post_comments)
    # print post_comments
    return render_template("post_comments.html", user_post=user_post, post_comments=post_comments)


@app.route("/posts/detail/comments/<int:post_id>", methods=['POST'])
def post_detail_comments_form(post_id):
    """Show details about a post and save comments."""

    # Get variables
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to access posts.")
        return redirect("/login")

    cid = request.form["comment_id"]
    parent = request.form["parent"]
    date_created = request.form["date_created"]
    # TODO: check if date_modified should be in another function or if loop
    # date_modified = request.form["date_modified"]
    content = request.form["content"]
    upvotes = request.form["upvote_count"]

    # TODO: iterate through form variables to eliminate blanks
    # TODO: iterate through form variables to verify data formats

    # comment = Comment(comment_id=comment_id, user_id=user_id, post_id=post_id, parent=parent,
    #                   date_created=date_created, date_modified=date_modified, content=content,
    #                   upvotes=upvote_count)
    comment = Comment(user_id=user_id, post_id=post_id, cid=cid, parent=parent,
                      date_created=date_created, content=content, upvotes=upvotes)
    db.session.add(comment)
    db.session.commit()
    flash("Comment added.")

    # return redirect("/posts/detail/%s" % post.post_id)

    # return render_template("post_comments.html", user_post=user_post, post_comments=post_comments)
    return jsonify({'status': 'success'})


@app.route("/posts/add", methods=['GET'])
def post_add_form():
    """Form to add a post."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to add posts.")
        return redirect("/login")

    return render_template("post_add.html")


@app.route("/posts/add", methods=['POST'])
def post_add():
    """Add a post."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to access posts.")
        return redirect("/login")
        # raise Exception("No user logged in.")

    # Get form variables
    event_date = request.form.get("event_date")
    ptype = request.form.get("ptype")
    topic = request.form.get("topic")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    vehicle_plate = request.form.get("vehicle_plate")

    # event_date = request.form["event_date"]
    # ptype = request.form["ptype"]
    # topic = request.form["topic"]
    # latitude = request.form["latitude"]
    # longitude = request.form["longitude"]
    # vehicle_plate = request.form["vehicle_plate"]

    print latitude, longitude

    vehicle_plate = vehicle_plate.upper()

    # if not (latitude and longitude):
    #     street = request.form["street"]
    #     city = request.form["city"]
    #     state = request.form["state"]
    #     zipcode = request.form["zipcode"]
    #     address = street + ", " + city + ", " + state + " " + zipcode

    # print address
    # location = Geocoder.geocode(address)
    # print location
    # print location.latitude
    # print location.longitude
    # print location[0]
    # print location[1]

    # vtype = request.form["vtype"]
    # make = request.form["make"]
    # model = request.form["model"]
    # color = request.form["color"]

    # TODO: iterate through form variables to eliminate blanks
    # TODO: iterate through form variables to verify data formats

    vehicle_check = Vehicle.query.filter_by(vehicle_plate=vehicle_plate).first()

    # vehicle must exist in db before post can be added
    if not (vehicle_check):
        vehicle = Vehicle(vehicle_plate=vehicle_plate, user_id_adder=user_id)
        # vehicle = Vehicle(vehicle_plate=vehicle_plate, vtype=vtype, make=make, model=model, color=color)
        db.session.add(vehicle)
        db.session.commit()

    post = Post(event_date=event_date, ptype=ptype, topic=topic, vehicle_plate=vehicle_plate, latitude=latitude, longitude=longitude, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    flash("Post added.")

    return redirect("/posts/detail/comments/%s" % post.post_id)


@app.route("/post_add.json", methods=['POST'])
def post_add_json():
    """Add a post."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to access posts.")
        return redirect("/login")
        # raise Exception("No user logged in.")

    # Get form variables
    event_date = request.form.get("event_date")
    ptype = request.form.get("ptype")
    topic = request.form.get("topic")
    latitude = request.form.get("latitude")
    longitude = request.form.get("longitude")
    vehicle_plate = request.form.get("vehicle_plate")

    # event_date = request.form["event_date"]
    # ptype = request.form["ptype"]
    # topic = request.form["topic"]
    # latitude = request.form["latitude"]
    # longitude = request.form["longitude"]
    # vehicle_plate = request.form["vehicle_plate"]

    print latitude, longitude

    vehicle_plate = vehicle_plate.upper()

    # if not (latitude and longitude):
    #     street = request.form["street"]
    #     city = request.form["city"]
    #     state = request.form["state"]
    #     zipcode = request.form["zipcode"]
    #     address = street + ", " + city + ", " + state + " " + zipcode

    # print address
    # location = Geocoder.geocode(address)
    # print location
    # print location.latitude
    # print location.longitude
    # print location[0]
    # print location[1]

    # vtype = request.form["vtype"]
    # make = request.form["make"]
    # model = request.form["model"]
    # color = request.form["color"]

    # TODO: iterate through form variables to eliminate blanks
    # TODO: iterate through form variables to verify data formats

    vehicle_check = Vehicle.query.filter_by(vehicle_plate=vehicle_plate).first()

    # vehicle must exist in db before post can be added
    if not (vehicle_check):
        vehicle = Vehicle(vehicle_plate=vehicle_plate, user_id_adder=user_id)
        # vehicle = Vehicle(vehicle_plate=vehicle_plate, vtype=vtype, make=make, model=model, color=color)
        db.session.add(vehicle)
        db.session.commit()

    post = Post(event_date=event_date, ptype=ptype, topic=topic, vehicle_plate=vehicle_plate, latitude=latitude, longitude=longitude, user_id=user_id)
    # print post
    db.session.add(post)
    db.session.commit()
    flash("Post added.")

    url = "/posts/detail/comments/"
    url = url + str(post.post_id)
    print url
    # return redirect("/posts/detail/comments/%s" % post.post_id)
    # return jsonify({'status': 'success'})
    return jsonify({'status': 'success', 'redirect': url})
    # return JSON(new {success=true, redirect=Url.Action("/")})


@app.route("/posts/edit/<int:post_id>", methods=['GET'])
def post_edit_form(post_id):
    """Render form to edit a post."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to access posts.")
        return redirect("/login")
        # raise Exception("No user logged in.")

    user_post = Post.query.filter_by(post_id=post_id, user_id=user_id).first()
    # user_post.event_date = user_post.event_date.strftime('%Y-%m-%d %I:%M %P')
    user_post.event_date = user_post.event_date.strftime('%Y-%m-%dT%H:%M')

    # vehicle = Vehicle.query.filter_by(vehicle_plate=user_post.vehicle_plate).first()

    # return render_template("post_edit.html", user_post=user_post, vehicle=vehicle)
    return render_template("post_edit.html", user_post=user_post)


@app.route("/posts/edit/<int:post_id>", methods=['POST'])
def post_edit(post_id):
    """Submit edits to a post."""

    user_id = session.get("user_id")

    if not user_id:
        flash("Please log in to access posts.")
        return redirect("/login")
        # raise Exception("No user logged in.")

    # Get form variables
    event_date = request.form["event_date"]
    ptype = request.form["ptype"]
    topic = request.form["topic"]
    # vehicle_plate = request.form["vehicle_plate"]
    # location = request.form["location"]

    # TODO: iterate through form variables to eliminate blanks
    # TODO: add ability to delete posts
    # TODO: fix ability to edit vehicle_plate
    post = Post.query.filter_by(post_id=post_id, user_id=user_id).first()

    if post:
        post.event_date = event_date
        post.ptype = ptype
        post.topic = topic
        # post.vehicle_plate = vehicle_plate
        # post.location = location
        flash("Post updated.")
    else:
        # post = Post(event_date=event_date, ptype=ptype, topic=topic, vehicle_plate=vehicle_plate, location=location, user_id=user_id)
        flash("Error updating post.")
        # db.session.add(post)

    db.session.commit()

    return redirect("/posts/detail/comments/%s" % post.post_id)


@app.route("/posts/vehicle/<vehicle_plate>", methods=['GET'])
def posts_by_vehicle(vehicle_plate):
    """Show posts for a vehicle."""

    posts = Post.query.filter_by(vehicle_plate=vehicle_plate).order_by(Post.event_date.desc()).limit(100).all()
    for post in posts:
        post.event_date = post.event_date.strftime('%m/%d/%Y %I:%M %P')
        user = User.query.filter_by(user_id=post.user_id).first()
        post.username = user.username

    return render_template("post_list.html", posts=posts)


# for heroku debugging
@app.route("/error")
def error():
    raise Exception("Error!")


if __name__ == '__main__':
    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # Create the tables we need from our models (if they already
    # exist, nothing will happen here, so it's fine to do this each
    # time on startup)
    db.create_all(app=app)

    # Use the DebugToolbar
    app.debug = False
    DebugToolbarExtension(app)
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    DEBUG = "NO_DEBUG" not in os.environ
    # app.run(port=5000, host='0.0.0.0')
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
