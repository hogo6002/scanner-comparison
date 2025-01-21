# Use the official Debian image as the base
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./src/requirements.txt .

# Install the Python dependencies and generate a lockfile (e.g., Pipfile.lock)
RUN pip install --no-cache-dir -r requirements.txt && pip freeze > requirements.lock

# Remove the lockfile
RUN rm requirements.lock

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run when the container starts
CMD ["python", "main.py"]