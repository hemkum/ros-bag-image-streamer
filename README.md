# ROS Image Streamer

## Project Overview

This project provides a Dockerized solution for streaming images from ROS bag files through a FastAPI backend to a frontend. It allows users to select topics from the corresponding bag file from a dropdown menu and view the associated images.
Backend developed with FastAPI, OpenCV, and ROS for processing and serving images. Frontend utilizes JavaScript to render these images dynamically. The backend converts these images to grayscale before streaming.


## Key Features

- **Dynamic Topic Selection**: Users can choose from a list of available topics provided by the backend, derived from the .bag file.
- **Grayscale Image Rendering**: Images are converted to grayscale in the backend for optimized viewing.
- **Client-Side State Management**: The frontend tracks and communicates the current image index.
- **Continuous Streaming**: Images are requested and rendered every 0.1 seconds, which can be modified at backend.

## Architecture

- **Backend (FastAPI, OpenCV, ROS)**: The backend is responsible for interfacing with ROS bag files, extracting and processing images, and serving them through RESTful APIs. It includes grayscale conversion using OpenCV and dynamic topic listing from ROS bag files.
- **Frontend (HTML, JavaScript)**: Provides a simple HTML and Javascript interface for topic selection and displaying streamed images. 
- **Docker**: Containers encapsulate the environment required to run the backend and serve the frontend.

## Setup and Running

### Prerequisites

- Docker installed on your machine.

### Building the Docker Image

To build the Docker image for the ROS Image Streamer, navigate to the project directory and execute:

```bash
docker build -t ros-image-streamer .
```

### Running the Docker image

```bash
docker run -p 8000:8000 ros-image-streamer
```

Open http://localhost:8000 in browser and choose topic to start streaming

## Improvement scope

Scope of improvement:
- Add multiple dropdown options in frontend to filter based on various criteria.
- Add buttons to start stop visualizations and navigate them witg back and forward buttons.
- Add functionality to adjust the playback speed of the visualizations
- add functionality to choose the ros bag file.
