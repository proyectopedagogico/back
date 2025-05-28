# Proyecto Pedagógico - Admin Backend

This is the backend administration panel for the "Proyecto Pedagógico". It is a Flask-based application designed to manage and serve content related to life stories, including people, images, tags, and their translations. It provides both a secure admin interface (via API) and public-facing API endpoints.
---

### Features

- **Admin Authentication**: Secure login for administrators using JWT (JSON Web Tokens).
- **Story Management**: Full CRUD (Create, Read, Update, Delete) operations for stories.
- **Multilingual Support**: Manages translations for story content.
- **People Management**: Stores information about the individuals whose stories are told.
- **Image Handling**: Allows uploading and associating images with people, including an upload folder and allowed extensions configuration.
- **Tagging System**: Categorizes stories using primary and many-to-many tags.
- **Public API**: Exposes stories to the public with filtering (by origin, profession, tag) and pagination.
- **Database Management**: Uses SQLAlchemy as an ORM and Flask-Migrate (Alembic) for handling database migrations.
- **Configuration Management**: Supports different environments (Development, Testing, Production).

## Technology Stack

- **Framework**: Flask
- **Database**: MySQL (using PyMySQL and mysqlclient drivers)
- **ORM**: Flask-SQLAlchemy
- **Migrations**: Flask-Migrate
- **Authentication**: Flask-JWT-Extended
- **CORS**: Flask-Cors
- **Password Hashing**: bcrypt
---

## Project Structure
  ```
proyectopedagogico/back/back-admin/
├── back_pedagogico/
│   ├── app/
│   │   ├── api/          # API Blueprints and routes
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   ├── image_routes.py
│   │   │   ├── public_routes.py
│   │   │   └── story_routes.py
│   │   ├── core/         # Core configurations
│   │   │   └── config.py
│   │   ├── models/       # SQLAlchemy models
│   │   │   ├── __init__.py
│   │   │   ├── admin_user_model.py
│   │   │   ├── image_model.py
│   │   │   ├── person_model.py
│   │   │   ├── story_model.py
│   │   │   ├── story_translation_model.py
│   │   │   └── tag_model.py
│   │   └── __init__.py   # Application factory
│   ├── migrations/       # Database migration scripts
│   ├── uploads/          # Folder for uploaded images (created on run)
│   ├── generate_admin_hash.py # Script to create admin password
│   └── run.py            # Application entry point
├── requirements.txt      # Python dependencies
└── README.md             # This file
  
  ```

---

##  Setup and Installation

###  Prerequisites

- Python 3.x
- MySQL Server

--- 

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd proyectopedagogico/back/back-admin/back_pedagogico
```

### 2. Create a Virtual Environment:
Bash
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies:
Bash
```
pip install -r requirements.txt
```

### 4. Configure Environment Variables:

Create a .env file in the back_pedagogico directory (or set environment variables directly).
    Define at least:
   ```
          SECRET_KEY: A strong secret key for Flask sessions and security.
     JWT_SECRET_KEY: A secret key for JWT signing.
     DEV_DATABASE_URL: Your MySQL connection string (e.g., mysql+pymysql://user:password@host:port/database_name).
     FLASK_CONFIG: Set to development, testing, or production. Defaults to development.
 ```

### Set up the Database:

 Ensure your MySQL server is running.
 Create the database specified in your DEV_DATABASE_URL.

### Run Migrations:

 Make sure you have set the FLASK_APP environment variable:
 Bash

export FLASK_APP=run.py # Or `set FLASK_APP=run.py` on Windows

### Apply the migrations:
Bash
  ```
 flask db upgrade
  ```
###  Create an Admin User:

 Run the generate_admin_hash.py script to create a secure password hash:
 Bash

     python generate_admin_hash.py
  ```
     Copy the generated hash.
     Manually insert a new record into the administrador table in your database, using your desired nombre_admin and the generated password_hash.
  ```
### Running the Application
  ```
 Ensure your virtual environment is active.
 Set the FLASK_APP environment variable (if not already set).
 Run the application:
 ```
 ```Bash

flask run
```

### Or directly using run.py:
```Bash

 python run.py
```
 The server will start, typically on http://0.0.0.0:5000/.

### API Endpoints
Admin Endpoints (Require JWT Authentication)

 POST /api/admin/login: Authenticate an admin user and get a JWT.
 POST /api/admin/logout: Log out an admin user (requires JWT).
 POST /api/stories: Create a new story.
 GET /api/stories: Get a list of all stories.
 GET /api/stories/<int:id>: Get details of a specific story.
 PUT /api/stories/<int:id>: Update a story.
 DELETE /api/stories/<int:id>: Delete a story.
 POST /api/persons/<int:id>/images: Upload an image for a person.
 (Other CRUD endpoints for Persons and Tags might exist or need to be added).

### Public Endpoints

 GET /api/public/stories: Get a paginated list of stories with filtering options (lang, page, per_page, procedencia, profesion, tag).
 GET /api/public/stories/<int:id>: Get details of a specific story.
 GET /api/uploads/<filename>: Serve uploaded images.
