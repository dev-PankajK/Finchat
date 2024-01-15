# Use the official Python image as the base image
FROM python:3.11

# Set environment variables for poetry
ENV POETRY_VERSION=1.7.1
ENV POETRY_HOME=/opt/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}

# Install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory to /app
WORKDIR /app

# Copy only the dependencies file to the container
COPY pyproject.toml poetry.lock /app/

# Install dependencies using poetry
RUN poetry install --no-root --no-dev

# Copy the local code to the container
COPY . /app/

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the application
CMD ["poetry", "run", "start"]
