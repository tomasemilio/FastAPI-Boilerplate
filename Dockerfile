# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt (or use Pipfile or pyproject.toml if you are using Poetry)
COPY requirements.txt .

# Install any required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port that FastAPI will run on
EXPOSE 8000

# Command to run the app
CMD ["python", "run.py"]
