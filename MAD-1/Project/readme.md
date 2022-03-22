# Local Setup
- Clone the project
- Run `local_setup.sh`

# Local Development Run
- `local_run.sh` It will start the flask app in `development`. Suited for local development
<!-- 
# Replit run
- Go to shell and run
    `pip install --upgrade poetry`
- Click on `main.py` and click button run
- Sample project is at https://replit.com/@thejeshgn/flask-template-app
- The web app will be availabe at https://flask-template-app.thejeshgn.repl.co
- Format https://<replname>.<username>.repl.co -->

# Folder Structure

- `app.py/(main.py in replit)` has the code for initializing and running the application.
- `local_setup.sh` has the script for setting up the local environment.
- `local_run.sh` has the script for running the application.
- `db_directory` folder has quantified_self1.sqlite3 database file.
- The `templates` folder has the html templates.
- `static` folder has two folders:
    - `img` folder has logo.png (logo of the application) and the trendlines will be saved here
    - `bootstrap` folder
        - `css` folder has all the styling code for html templates
- `application` folder has the below:
    - Initialized database in `database.py`
    - Implemented database models in `model.py`
    - All the application controllers are implemented in `controllers.py`
    - Configurations are implemented in `config.py`
    - Implemented the apis in `api.py`
    - Implemented custom exceptions in `validations.py`


```
├── application
│   ├── config.py
│   ├── controllers.py
│   ├── database.py
│   ├── __init__.py
│   ├── models.py
|   |__ api.py
|   |__ validations.py
│   └── __pycache__
│       ├── config.cpython-36.pyc
│       ├── config.cpython-37.pyc
│       ├── controllers.cpython-36.pyc
│       ├── controllers.cpython-37.pyc
│       ├── database.cpython-36.pyc
│       ├── database.cpython-37.pyc
│       ├── __init__.cpython-36.pyc
│       ├── __init__.cpython-37.pyc
│       ├── models.cpython-36.pyc
│       └── models.cpython-37.pyc
├── db_directory
│   └── quantified_self1.sqlite3
├── local_run.sh
├── local_setup.sh
├── app.py
├── readme.md
|__ requirements.txt
├── static
│   ├── bootstrap
│   │   ├── css
│   │   │   ├── addtracker.css
│   │   │   ├── create.css
│   │   │   ├── dashboard.css
│   │   │   ├── index.css
│   │   │   ├── logevent.css
│   │   │   ├── login.css
│   │   │   ├── myprofile.css
│   │   │   ├── tracker.css
│   │   │   
|   |-- img
|   |   |__ logo.png
└── templates
    └── index.html
    |__ create.html
    |__ addtracker.html
    |__ dashboard.html
    |__ logevent.html
    |__ login.html
    |__ myprofile.html
    |__ tracker.html
    |__ updatelog.html
    |__ updatetracker.html
    |__ aboutus.html
```