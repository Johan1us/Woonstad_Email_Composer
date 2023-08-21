# Use the official Python 3.11 image
FROM python:3.11-slim-buster

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create a working directory
WORKDIR /app

# Install the required dependencies
RUN pip install --no-cache-dir streamlit==1.23.1 openai==0.27.8

# Copy your files into the container
COPY utils/ utils/
COPY pages/ pages/
COPY .streamlit/config.toml .streamlit/config.toml
COPY app.py app.py

# Command to run your application
CMD ["streamlit", "run", "app.py", "--server.port", "8080"]
