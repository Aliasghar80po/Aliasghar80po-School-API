# استفاده از یک تصویر پای# Use an official Python runtime as a parent image
FROM python:3.11.4

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE myproject.settings

# Set work directory
WORKDIR /code

# Copy the current directory contents into the container at /code
COPY . /code/

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Run migrations
RUN python manage.py migrate

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD while ! python3 manage.py sqlflush > /dev/null 2>&1 ; do sleep 1 ; done && \
    python3 manage.py makemigrations --noinput && \
    python3 manage.py migrate --noinput && \
    python3 manage.py collectstatic --noinput && \
    python3 manage.py createsuperuser --user sepehr --email shahberger@gmail.com --noinput; \
    gunicorn -b 0.0.0.0:8000 config.wsgi