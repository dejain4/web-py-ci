# Use an official Python runtime as a parent image
FROM python:3.11.3-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy poetry.lock and pyproject.toml to working directory
COPY poetry.lock pyproject.toml ./

# Install dependencies using Poetry
RUN pip install poetry && \
    poetry config virtualenvs.create false

# Install dependencies with production flag
RUN poetry install --no-interaction --no-ansi --no-root --only=main

# Set the environment variable for Flask app
ENV FLASK_APP=app

# Copy the rest of the application code
COPY /src .

# Expose port 5000 for the Flask application to listen on
EXPOSE 5000

# Start the Flask application with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
