# Set base image (host OS)
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /code

# Create a new user with UID
RUN adduser --disabled-password --gecos '' --system --uid 1001 python && chown -R python /code

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY main.py .

# Set user to newly created user
USER 1001

# Command to run on container start
CMD [ "python", "main.py" ]
