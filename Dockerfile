#######
# Use an official lightweight Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for building certain Python packages
RUN apt-get update && apt-get install -y gcc g++ python3-dev && rm -rf /var/lib/apt/lists/*

# Copy the backend code and requirements file into the container
COPY ./backend /app/backend

#install the general Python dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# # Install ROS bag package separately with the extra index URL
# RUN pip install --extra-index-url https://rospypi.github.io/simple/ rosbag

# Copy the frontend code into the container
COPY ./frontend /app/frontend

# Copy the bag data into the container
COPY ./bag_data /app/bag_data

# Expose the port the app runs on
EXPOSE 8000

# command to run the application
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--reload"]
