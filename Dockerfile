# Base image: lightweight Python 3.10 environment
FROM python:3.10-slim

# Set working folder inside the container
WORKDIR /app

# Copy dependency list and install packages first (for faster rebuilds)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Command that runs when the container starts
CMD ["python", "Day4Task.py"]