# Use the official Python image from DockerHub as a base image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port that Streamlit uses (default is 8501)
EXPOSE 8501

# Set environment variables for Streamlit (fixing the format warning)
ENV STREAMLIT_SERVER_HEADLESS=true

# Command to run your Streamlit app
CMD ["streamlit", "run", "main.py"]
