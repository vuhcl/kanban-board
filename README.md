# Kanban Board

## Functionality

This web app provides a kanban board with a simple three-step workflow. The board the divided into three columns, each marked with a step in the working process: to do, doing, or done. Each user has their own kanban board and can create new tasks, move tasks to different states, or delete the tasks.

## File Structure

The root directory contains the following files:

- `test.py` contains the unittests.
- `requirements.txt` contains the required packages for the project.
- `app.py` gets the app to run.

The `app` folder contains the application files:

- `__init__.py` contains the configuration and initializes the app.
- `api.py` contains routes which serves frontend pages made up of HTML and CSS.
- `models.py` connects to the database and contains the SQLAlchemy tables.
- `static/` is a folder which contains static assets for the frontend: CSS style sheets, images, etc.
- `templates/` is a folder which contains html templates to be rendered.

This is based on [this structure](http://flask.pocoo.org/docs/0.12/patterns/packages).
