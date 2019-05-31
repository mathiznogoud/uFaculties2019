# uFaculties - A web application for information searching.

### How to build

**Clone this repo**
```
$ git clone https://github.com/mathiznogoud/uFaculties2019.git
```


**Need to install virtualenv**

```
$ sudo apt-get install virtualenv
```

**Then navigate to the project directory, create a new virtual environment**
```
$ virtualenv -p python3 env
```

**Activate virtual environment**
```
$ source env/bin/activate
```

**Install plugins, dependencies to build the project**
```
$ pip install -r requirements.txt
```



## Database

#### Install MySQL database, MySQL Workbench for database management
```
https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04
```

#### Need to create a new database (MySQL Database)

```
$ sudo mysql -u root -p

mysql> CREATE USER 'your_dbusername'@'localhost' IDENTIFIED BY 'your_password';
Query OK, 0 rows affected (0.00 sec)

mysql> CREATE DATABASE uFaculties_db;
Query OK, 1 row affected (0.00 sec)

mysql> GRANT ALL PRIVILEGES ON uFaculties_db . * TO 'your_dbusername'@'localhost';
Query OK, 0 rows affected (0.00 sec)
```

#### Config your database in **_instance/config.py_**
```
SQLALCHEMY_DATABASE_URI = 'mysql://your_dbusername:your_password@localhost/uFaculties_db'

### Existing config
```


# Run the project
Navigate to the directory that have **_run.py_**
Activate virtualenv
```
$ source env/bin/activate
```

### Set the FLASK_CONFIG and FLASK_APP environment variables before running the app:
```
$ export FLASK_CONFIG=development
$ export FLASK_APP=run.py
$ flask run
 * Serving Flask app "run"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```



# TODO list:
**1. Create a TreeView for ```researchfields``` with create, delete, update operations on the tree. Update the database after edit the tree** (NOT DONE YET)


**2. Create an unique user profile for every teacher. Define routes and rebuild the database models to fit in the user profile properties (Build with RESTFul API)** (NOT DONE YET)

