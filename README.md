
[![Build Status](https://travis-ci.org/RachaelNantale/accrual-system.svg?branch=develop)](https://travis-ci.org/RachaelNantale/accrual-system)
[![Coverage Status](https://coveralls.io/repos/github/RachaelNantale/accrual-system/badge.svg?branch=develop)](https://coveralls.io/github/RachaelNantale/accrual-system?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/1aeba998d3eb93fe3104/maintainability)](https://codeclimate.com/github/RachaelNantale/accrual-system/maintainability)
# Accrual System - Managing Employee Benefits

## Description

Each month an employee earns they earn a set amount of points depending upon a) their role and
b) their tenure at Fenix.
Points can be redeemed for a variety of benefits from gym membership fees, to additional days of
PTO.

## Features

- Users can create an account and log in.
- Users can create a request


## Main requirements include:

> 1. [git](https://git-scm.com/)
> 2. [python](https://docs.python.org/)
> 3. [pip](https://pypi.python.org/pypi/pip)
> 4. [virtualenv](https://virtualenv.pypa.io/en/stable/)
> 5. [python-crontab](https://pypi.org/project/django-crontab/)

## Set up of the App

1. Clone the project

`https://github.com/RachaelNantale/accrual-system.git`

2. Navigate to the project directory

`cd accrual_system`

3. Create a virtual environment using `virtualenv` and activate it.
     `virtualenv env`
    `source env/bin/activate` for `Unix`
    `source env/bin/activate` for `Windows`

4. Install packages using `pip install -r requirements.txt`



#### Instructions on using the .env file for setting up the database

- the system uses `sqllite` which is set up in the `settings.py` already.
- run `python manage.py makemigrations` to create the migrations
- run `python manage.py migrate` to add the migrations to the app

6. Run the app by running `manage.py`

`python manage.py runserver`

7. Run Tests

`python manage.py test`

