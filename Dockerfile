# Use an official Python runtime as a parent image
FROM python:3.13-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy the Flask app files
COPY . .

# Expose port 5000 for Flask
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--reload"]
# CMD ['python', 'app.py']
