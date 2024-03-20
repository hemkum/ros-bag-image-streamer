from fastapi import FastAPI, HTTPException, Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import io
import rosbag
import numpy as np

# Path to the ROS bag file
BAG_PATH = 'bag_data/instruction1.bag'

# Initialize app
app = FastAPI()

#Configure CORS for cross-origin allowance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#  endpoint for root
@app.get("/")
async def read_root():
    return FileResponse('frontend/index.html')

# Mount other static files
app.mount("/ui", StaticFiles(directory="frontend", html=True), name="frontend")


# Function to list available topics from the ROS bag
def list_topics():
    try:
        bag = rosbag.Bag(BAG_PATH)
        topics = bag.get_type_and_topic_info()[1].keys()
        bag.close()
        return list(topics)
    # Handle errors during listing
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"ROS bag file '{BAG_PATH}' not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing topics: {str(e)}")

# Function to get an image by topic and index from the ROS bag
def get_image_by_index(topic, index):
    try:
        bag = rosbag.Bag(BAG_PATH)
    except FileNotFoundError:
        return None, "ROS bag file not found."
    except Exception as e:
        return None, f"Error opening ROS bag: {str(e)}"

    found_image = None
    try:
        # Iterate through ros messages for the specified topic
        for i, (_, msg, _) in enumerate(bag.read_messages(topics=topic)):
            if i == index:
                # Try to convert message data to an image array
                try:
                    img_array = np.frombuffer(msg.data, dtype=np.uint8).reshape(msg.height, msg.width, -1)
                    found_image = img_array
                    break
                except Exception as e:
                    return None, "Failed to extract image."
        else:
            return None, "Index out of range."
    finally:
        bag.close()
    return found_image, None if found_image is not None else "Image not found."

# API endpoint to list topics
@app.get("/api/topics")
async def topics():
    # Return topics list as JSON
    try:
        topics = list_topics()
        return {"topics": topics}
    # Pass on HTTPException and handle unexpected errors
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# API endpoint to get images by topic and index
@app.get("/api/image/{topic:path}/{index}")
async def image(topic: str, index: int):
    image, error = get_image_by_index(topic, index)
    if image is None:
        raise HTTPException(status_code=404, detail=error or "Image not found.")
    try:
        # Convert the image from BGR color to grayscale using cvtColor 
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Encode and store grayscale image into a JPEG format 
        _, buffer = cv2.imencode('.jpg', image_gray)

        # streams the image stored in the 'buffer' as BytesIO instance directly to the client
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
