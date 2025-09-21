# Mixologist Server

Mixologist is a backend server for registering and retrieving cocktail recipes. It provides a RESTful API for managing cocktails, ingredients, tags, and related data.

## Tech Stack
- Python 3 (with Flask)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- PostgreSQL (database)
- Flake8 & Black (linting/formatting)

## Setup Instructions

### 1. Create and Activate Virtual Environment
Inside the server directory, run the following commands to activate the virtual environment:
```
python -m venv .venv
source .venv/bin/activate
```

### 2. Install Dependencies
With your environment activated, install the python dependencies by running pip:
```
pip install -r requirements.txt
```

### 3. Install PostgreSQL & psycopg2
This project uses PostgreSQL as its database system, and psycopg as its driver. Before setting up a local database you will need to:
- Install PostgreSQL from your OS package manager or official website
- psycopg2 is already included in requirements.txt

When installing PostgreSQL, it is also recommended to install pgAdmin so you can access and inspect the DB, as well as be able to run queries outside of the server.

### 4. Configure the Database

- Create a PostgreSQL database and user (any db name, port, user and password you prefer). Note those down.
- Create a `.env.development` file in the `./server` directory and populate it with your database connection details noted above. The file must have the following variables: 
  ```
  DB_HOST=localhost
  DB_PORT=5432
  DB_NAME=your_db_name
  DB_USER=your_db_user
  DB_PASSWORD=your_db_password
  ```
- These values will be read by `settings.py` to connect to your local database.

### 5. Database Migrations with Alembic

As mentioned above, this project runs with SQLAlchemy, a widely used ORM (Object-Relational Mapping) tool in the industry.

You can create new tables classes by using the BaseModel class, or update and expand existing models as the project grows. When you do so, we need to update the DB to reflect any table changes, table drops or creations.

This is when Alembic comes into play, as it allows you to automatically create version control scripts in Python. These scripts will run the necessary database queries to update your schema changes.

- The project is pre-configured for Alembic auto-revisions.
- To create a new migration after model changes:
  ```
  alembic revision --autogenerate -m "Describe your change"
  ```
- To apply migrations (upgrade):
  ```
  alembic upgrade head
  ```
- To revert migrations (downgrade):
  ```
  alembic downgrade -1
  ```

## Linting & Formatting
You can format your code by running the following commands:

- Run `flake8 src/` to check code style.
- Run `black src/` to auto-format code.

Pre-commit hooks are set up to enforce these checks before every commit. You may need to configure your IDE if you want to have linting on save. If using VSCode, install the Black addon and following instructions on the addon page.

## Next Steps

- **Add Flask Endpoints:**
  - Implement a Flask server with RESTful endpoints for interacting with the database (CRUD operations for cocktails, ingredients, steps, etc.).
  - Organize the codebase using the MVC (Model-View-Controller) pattern for maintainability and scalability.

- **Create and Load Test Data:**
  - Prepare a test database of ingredients, cocktails, and steps.
  - Use pandas to load this data into the database for development and testing purposes.

These steps will help expand the project into a fully functional API and provide sample data for development and testing.

---

