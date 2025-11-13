 # Dockerfile
# Use a lightweight Python base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application code
COPY . .

# Expose the port your Flask app runs on (default is 5000)
EXPOSE 8080

# Command to run the Flask application using Gunicorn for production
# For development, you can use `flask run --host=0.0.0.0`
#CMD ["ls"]
CMD ["waitress-serve", "--call", "eCardCreator:create_app"]