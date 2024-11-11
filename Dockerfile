# Slim python version
FROM python:3.12-slim-bookworm

#Defined workdir
WORKDIR /app

#Copy only th requirements
COPY requirements/dev.txt /app/requirements/dev.txt

# Install playweight dependencies for the system
RUN apt-get update && apt-get install -y \
    libgsf-1-114 \
    libxss1 \
    libgtk-3-0 \
    libdbus-glib-1-2 \
    && rm -rf /var/lib/apt/lists/*

# Install python deps
RUN pip install --no-cache-dir -r /app/requirements/dev.txt

# Install playweight dependencies
RUN playwright install --with-deps

# Copy the project
COPY . /app/
