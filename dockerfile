# Use official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock (if available)
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-dev --no-interaction --no-ansi

# Copy the rest of the application code to the container
COPY . /app

# Run the app
CMD ["poetry", "run", "python", "inventery.py"]
