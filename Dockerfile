FROM python:3.10.2-alpine

# Does not allow python to buffer outputs
# Improves performance and allows viewing container logs in real time
ENV PYTHONUNBUFFERED 1

# Prevent python from writing bytecode files to disk
# Improve performance and keeps development env clean
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /pokedex-api

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy code after installing dependencies to best utilize Docker cache
COPY ./app ./app

# Create a user that can only run apps for security purposes
RUN adduser -D user
USER user