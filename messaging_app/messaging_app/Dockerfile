# Use official Python image as base
FROM python:3.10

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port (Django default = 8000)
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "messaging_app.wsgi:application", "--bind", "0.0.0.0:8000"]

