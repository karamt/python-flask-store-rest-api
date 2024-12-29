## Flask Python App with SQLAlchemy

### Running the flask app locally using Docker
    docker run -p **local_port**:5000 -w /app -v "$(pwd):/app" **Docker_Image_name** sh -c "flask run --host 0.0.0.0"

    This is similar to how we've ran the Docker container with our local code as a volume (that's what -w /app -v "$(pwd):/app" does), but at the end of the command we're telling the container to run flask run --host 0.0.0.0 instead of the CMD line of the Dockerfile. That's what sh -c "flask run --host 0.0.0.0" does!

### Running the flask app locally using gunicorn
    docker run -p **local_port**:80 **Docker_Image_name** 
    
    Note: Here we cannot map the local /app directory to a volume in order to reflect our code changes right away. Reason is gunicorn is good for production mode. We can do this with flask as we are running flask in dev mode

### Running docker container with volume mounting on code files (docker file has gunicorn command which we are overriding here)
    docker run -p 8000:5000 -w /app -v "$(pwd):/app" store-flask-smorest-api sh -c "flask run --host 0.0.0.0"

### Running flask app locally
    flask run --host 0.0.0.0 --port 8000
    OR 
    flask run -h 0.0.0.0 -p 8000

### Bulding docker compose web service forcefully (if say some modules are added to requirements.txt after last docker compose build)
    docker compose up --build --force-recreate --no-deps web

### How to run the database migrations in your compose container
    First run the compose file with 
        docker compose up -d
    Then run the database upgrade command with 
        docker compose exec web flask db upgrade

### Deleting docker volumes using docker compose
    docker compose down -v

### Flask migrate commands
    flask db init
    flask db migrate
    flask db upgrade
    flask db downgrade

### Create .env file in root folder if say want to use another db like postgres (by defualt application uses SQLite) with below contents
    DATABASE_URL=postgresql://db_username:db_password@db_service/db_name
    for eg
    DATABASE_URL=postgresql://postgres:password@db/postgres

    For connecting to local postgress db use below
    DATABASE_URL=postgresql://db_postgres:db_password@**localhost**/postgres