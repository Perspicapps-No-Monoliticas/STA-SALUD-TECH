# Use the official Python image from the Docker Hub
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements first to leverage Docker cache
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code into the container
COPY . .

# Command to run the consumer
CMD ["python", "consumidores.py"]