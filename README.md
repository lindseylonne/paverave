# PaveRave!

http://www.paverave.com
Enter a vehicle license plate, and create a post. Comment and upvote. Sort and search. 
Use for good or evil as you see fit... just keep the paverage online and off the streets, please!
More to come: Heat map, mobile app, social features like badges and carma points. 
Stay tuned! Email news@paverave.com with "subcribe" in the subject to receive notification of new features.

(I created the initial version of this, my first solo project - in 2 sprints and approximately 80 hours - as part of an accelerated programming course at Hackbright Academy. Feedback is welcome and encouraged!)

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Optional: Use whatever dev tools you prefer. We used these tools:

* [Git Bash](https://git-for-windows.github.io/)
* [Vagrant Virtual Machine](https://www.vagrantup.com/downloads.html)
* [Sublime Text 2](https://sublimetext.com/2)
* [SublimeLinter plugin](https://sublime.wbond.net/installation#st2)

```
install git bash if you're using Windows
install vagrant accepting defaults
open git bash or your linux command line
cd to your home directory
mkdir vagrant
mkdir src
cd vagrant (download/unpack the vagrant setup files for your system to this folder)
vagrant up
vagrant ssh
cd src
mkdir paverave
cd paverave
virtualenv env (create your enviroment)
source env/bin/activate (--always-copy if on Windows)
```

### Installing

[Fork the paverave repository, then clone it to your local project directory.](https://guides.github.com/activities/forking/)

```
git init
```

Install the required packages listed in 
[requirements.txt](https://github.com/lindseylonne/paverave/blob/master/requirements.txt)

```
pip install < requirements.txt
```

Crete the database:

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
Open your browser of choice and go to: http://localhost:5000
```

## Running the tests (loading...)

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests (loading...)

Explain what these tests test and why

```
Give an example
```

## Deployment (loading...)

Add additional notes about how to deploy this on a live system

## Built With

Python, Javascript, PostgreSQL, and...
* [Flask](http://flask.pocoo.org/) - Flask is a microframework for Python based on Werkzeug, Jinja 2.
* [Jinja2](http://jinja.pocoo.org/) - Full featured template engine for Python.
* [SQLAlchemy](http://www.sqlalchemy.org/) - Python SQL toolkit and Object Relational Mapper.
* [jquery-comments](http://viima.github.io/jquery-comments) - JQuery comments plugin with reply and upvote.
* [DataTables](https://datatables.net/) - JQuery plugin for table generation with search and sort.
* [argon2](http://argon2-cffi.readthedocs.io/en/stable/argon2.html) - Used for password hashing.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/lindseylonne/paverave/blob/master/CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/lindseylonne/paverave/tags). 

## Authors

* **Lindsey Lonne** - *Initial work* - [lindseylonne](https://github.com/lindseylonne)

See also the list of [contributors](https://github.com/lindseylonne/paverave/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/lindseylonne/paverave/blob/master/LICENSE.md) file for details

## Acknowledgments

* Heartfelt thanks to the amazing staff at [Hackbright Academy](https://hackbrightacademy.com/). I could not have done this without your tireless dedication and support!
* Much love to my Hackbright cohort mates in Ada Winter 2017. Thank you for the friendship and inspiration!
* Deepest gratitude to my family and friends for their patience while I dropped off the face of the planet for a few weeks.