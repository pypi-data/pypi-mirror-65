# Vote4Film

Simplify film selection for regular film nights. Participants can:

- Add films
- Vote for films
- Declare absences
- See the schedule which takes into account votes and absences

Admins can set the schedule of film nights.

This is a simple WSGI Web Application. The back-end is Django, and the front-end
is dynamic HTML served by Django (no JavaScript is used).

## Development

1. `poetry install` to set-up the virtualenv (one-off)
2. `poetry run ./src/manage.py migrate` to set-up the local DB (one-off)
3. `poetry run ./src/manage.py runserver_plus`
4. `make fix`, `make check` and `make test` before committing

### Contributing

Pull requests are welcome :)

TODO: Fix dependency on `bbfcapi` to be `bbfcapi[apis]` and remove direct
dependency on `pyhumps`.

### Publishing

This application is published on PyPi.

1. Ensure you have configured the PyPi repository with Poetry (one-off)
2. Add the release notes in this README.md
3. `poetry version minor` to bump the major/minor/patch version
4. Also bump version in `vote4film/__init__.py`
4. `poetry publish --build` to release

To publish to the test repository:

1. Ensure you have configured the Test PyPi repository with Poetry (one-off)
2. `poetry publish --build -r testpypi` to upload to the test repository

## Deployment

Unfortunately, I will not provide detailed guidance for production deployment.

Some general tips:

* Create a virtualenv, e.g. in `~/virtualenv`
* Install with `pip install vote4film[postgres]`
* Write the configuration at `~/.config/vote4film/local.env`
* Use Postgres as the database
* Use Nginx/uWSGI to to serve the site (with HTTPS)
* Run Django management commands using `./virtualenv/bin/manage`

## Changelog

### Unpublished

...

### v1.5.2 - 2020-04-04

- Fix link to calender when there is no upcoming event

### v1.5.1 - 2020-04-04

- Fix call-to-action flow for the upcoming page

### v1.5.0 - 2020-04-04

- Overhaul user interface
- Enable additional Sentry features including tracing

### v1.4.0 - 2020-03-22

- Allow users to change their vote
- Redirect the user to the schedule after registering for the event
- Hide upcoming film until the user has voted for all films
- Add actually usable admin interface
- Add optional Sentry integration

### v1.3.0 - 2020-03-22

- Fix error adding film when age rating on IMDB/OMDB is "N/A"
- Add BBFC age ratings

### v1.2.3 - 2020-02-01

- Redirect to upcoming schedule after voting for every film
- Fix HTTP 500 error when on schedule page without registering for the event

### v1.2.2 - 2019-12-05

- Fix HTTP 500 error when adding a film that was already added (again)
- Highlight calender and vote links when there is a user action to take
- Pick the oldest added film for upcoming when scores are a draw

### v1.2.1 - 2019-11-21

- Remove "film is not available" from the voting page
- Remove "vote for this film" from the voting page
- Fix the upcoming page asking absent users to register on calender

### v1.2.0 - 2019-11-21

- Fix ranking films with zero votes as number one
- Hide upcoming film until the user has registered for the next event
- Clarify what will happen when adding a film by giving the user more choices
- Fix HTTP 500 error when adding a film that was already added
- Hide a film's votes from the user until they have voted

### v1.1.0 - 2019/11/16

- Show the register of present/absent users for upcoming films
- Fix not highlighting films that are not available to be watched
- Fix parsing of "Not Rated" age ratings resulting in an error

### v1.0.9 - 2019/11/13

- Actually let's not be too dumb about packaging

### v1.0.8 - 2019/11/13

- Rename management command from vote4film to manage
- Stop trying to be smart about packaging

### v1.0.7 - 2019/11/13

- The same fixes as v1.0.6 but for real this time

### v1.0.6 - 2019/11/13

- Fix url patterns for internal apps in installed environment
- Fix missing template files in PyPi package (so typical!)

### v1.0.5 - 2019/11/12

- Add optional postgres support, e.g. `pip install vote4film[postgres]`

### v1.0.4 - 2019/11/12

- Fix bug loading config from XDG config home (sigh)
- Fix django-extensions being missed from dependencies

### v1.0.3 - 2019/11/12

- Fix config sub-directory used in XDG config home

### v1.0.2 - 2019/11/12

- Load configuration from XDG config home

### v1.0.1 - 2019/11/10

- First release of Vote4Film
