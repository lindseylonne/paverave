# PaveRave!

https://www.paverave.com
http://paverave.herokuapp.com/

PaveRave is a social app that allows you to have conversations with other drivers.
Enter a vehicle license plate, and create a post.
Comment and upvote posts.
Sort and search on license plate or user.
View posts on a map.

More to come: 
* Mobile app with license plate image recognition. 
* More social features like badges and carma points. Tagging users, messaging, and chat.

Stay tuned! Email news@paverave.com with "subcribe" in the subject to receive notification of new features.

(This is my first full stack solo project with Python. It was created in 4 weeks (5 hours a day, M-F) as part of an accelerated programming course at Hackbright Academy. Feedback is welcome and encouraged!)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

* Python 2.* (with pip)
* PostgreSQL
* your Google Maps API key (If you want to use the map feature.)
* Your favorite dev setup
* the rest is installed from requirements.txt below

### Installing Locally

[Clone the paverave repo to your local project directory.](https://help.github.com/articles/cloning-a-repository/)

```
cd paverave
git clone https://github.com/lindseylonne/paverave
```

Install the required packages listed in 
[requirements.txt](https://github.com/lindseylonne/paverave/blob/master/requirements.txt)

```
pip install < requirements.txt
```

Create the database:

```
python -i model.py
>>> db.create_all()
```

Start the Flask server:

```
python server.py
```

Behold the wonder:

```
http://localhost:5000
```

## Running the tests (loading...)

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Insert example
```

### And coding style tests (loading...)

Explain what these tests test and why

```
Insert example
```

## Deployment (loading...)

### Heroku:

* create a free [account on heroku](https://www.heroku.com/)
* install the [heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)

```
$ cd (your paverave git project dir)
$ heroku login
$ heroku apps:create "nameofyourapp"
$ heroku git:remote -a "nameofyourapp"
$ git remote -v // to confirm
$ git push heroku master
$ heroku config:set NO_DEBUG=1
$ heroku config:set GOOGLE_MAPS_API_KEY="your api key"
$ heroku config:set FLASK_SECRET_KEY="choose your key"
$ heroku addons:create heroku-postgresql
$ heroku config // should show everything you just entered
$ heroku pg:psql // allows access to your new DB
$ git push heroku master
$ heroku open // should launch http://(nameofyourapp).herokuapp.com/
```

## Built With

Python, Javascript, PostgreSQL, and...
* [Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2.
* [Jinja2](http://jinja.pocoo.org/) - Full featured template engine for Python.
* [SQLAlchemy](http://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper.
* [jquery-comments](http://viima.github.io/jquery-comments) - JQuery comments plugin with reply and upvote.
* [DataTables](https://datatables.net/) - JQuery plugin for table generation with search and sort.
* [argon2](http://argon2-cffi.readthedocs.io/en/stable/argon2.html) - Used for password hashing.
* [Google Maps Javascript API](https://developers.google.com/maps/documentation/javascript/) - Showing locations of posts

## Contributing

Please read [CONTRIBUTING.md](https://github.com/lindseylonne/paverave/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests.

## Versioning

This project uses [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/lindseylonne/paverave/tags). 

## Authors

* **Lindsey Lonne** - *Initial work* - [lindseylonne](https://github.com/lindseylonne)

See also the list of [contributors](https://github.com/lindseylonne/paverave/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/lindseylonne/paverave/blob/master/LICENSE.md) file for details

## Acknowledgments

* Heartfelt thanks to the amazing staff at [Hackbright Academy](https://hackbrightacademy.com/). I could not have done this without your dedication and support!
* Much love to my Hackbright cohort mates in Ada Winter 2017. Thank you for the friendship and inspiration!
* Deepest gratitude to my family and friends for their patience while I dropped off the face of the planet for a few weeks.
