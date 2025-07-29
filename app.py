import streamlit as st
import cv2
import torch
from ultralytics import YOLO
import numpy as np
import time
import pygame  # For alarm sound

# Initialize pygame mixer for sound
pygame.mixer.init()

# Load alarm sound (Make sure you have an alarm.mp3 or any alarm sound in the specified directory)
ALARM_SOUND_PATH = r"cyber-alarms-synthesized-116358.mp3"

# Set a fixed random seed for reproducibility
seed = 42
torch.manual_seed(seed)

# Load the YOLO model (update the model path)
model = YOLO(r"best.pt")  # Your model path

# Alarm Sound function
def play_alarm():
    pygame.mixer.music.load(ALARM_SOUND_PATH)  # Load alarm sound
    pygame.mixer.music.play()  # Play alarm sound
    st.warning("⚠️ Fire detected! Alarm triggered!")

# Draw a rounded rectangle
def draw_rounded_rectangle(image, start_point, end_point, color, thickness):
    radius = 20  # Radius for rounded corners
    cv2.rectangle(image, start_point, end_point, color, thickness, lineType=cv2.LINE_AA, shift=0)
    cv2.circle(image, (start_point[0] + radius, start_point[1] + radius), radius, color, thickness, lineType=cv2.LINE_AA)
    cv2.circle(image, (end_point[0] - radius, start_point[1] + radius), radius, color, thickness, lineType=cv2.LINE_AA)
    cv2.circle(image, (end_point[0] - radius, end_point[1] - radius), radius, color, thickness, lineType=cv2.LINE_AA)
    cv2.circle(image, (start_point[0] + radius, end_point[1] - radius), radius, color, thickness, lineType=cv2.LINE_AA)

def process_image(image):
    if image.shape[2] == 4:  # Check if the image has an alpha channel
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    results = model(image)
    
    fire_detected = False

    for result in results:
        boxes = result.boxes
        for box in boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])
            class_name = model.names[class_id].lower()

            # Fire detected, draw rounded rectangle
            fire_detected = True
            color = (0, 0, 255)  # Red for fire
            draw_rounded_rectangle(image, (x1, y1), (x2, y2), color, 5)  # Draw rounded rectangle around fire

            # Draw label
            label = "Fire Detected"
            cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Trigger alarm if fire is detected
    if fire_detected:
        play_alarm()
    
    return image

# Function to capture from the laptop camera in real-time
def run_camera():
    cap = cv2.VideoCapture(0)  # Access laptop camera
    stframe = st.empty()  # Placeholder for the video stream

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.write("Camera not working!")
            break
        
        annotated_frame = process_image(frame)
        
        # Display the frame in Streamlit
        stframe.image(annotated_frame, channels="BGR", use_column_width=True)

        # Add a small delay to control the frame rate
        time.sleep(0.03)

# Streamlit app interface
st.title("Fire Detection with Alarm System")

# Start real-time camera feed
if st.button('Start Camera'):
    run_camera()

# Stop alarm when user presses the button
if st.button('Stop Alarm'):
    pygame.mixer.music.stop()











# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# import streamlit as st
# import cv2
# import torch
# from ultralytics import YOLO
# import numpy as np
# import time
# import pygame  # For alarm sound

# # Initialize pygame mixer for sound
# pygame.mixer.init()

# # Load alarm sound (Make sure you have an alarm.mp3 or any alarm sound in the specified directory)
# ALARM_SOUND_PATH = r"C:\Users\Admin\Downloads\Fire_Detection\cyber-alarms-synthesized-116358.mp3"

# # Set a fixed random seed for reproducibility
# seed = 42
# torch.manual_seed(seed)

# # Load the YOLO model (update the model path)
# model = YOLO(r"C:\Users\Admin\Downloads\Fire_Detection\best (1).pt")  # Your model path

# # Alarm Sound function
# def play_alarm():
#     pygame.mixer.music.load(ALARM_SOUND_PATH)  # Load alarm sound
#     pygame.mixer.music.play()  # Play alarm sound
#     st.warning("⚠️ Fire detected! Alarm triggered!")

# # Draw a rounded rectangle
# def draw_rounded_rectangle(image, start_point, end_point, color, thickness):
#     """Draw a rounded rectangle on an image."""
#     x1, y1 = start_point
#     x2, y2 = end_point

#     # Draw rectangle edges
#     cv2.rectangle(image, (x1 + 20, y1), (x2 - 20, y2), color, thickness)  # Top edge
#     cv2.rectangle(image, (x1, y1 + 20), (x2, y2 - 20), color, thickness)  # Side edges

#     # Draw rounded corners
#     cv2.circle(image, (x1 + 20, y1 + 20), 20, color, thickness)  # Top left corner
#     cv2.circle(image, (x2 - 20, y1 + 20), 20, color, thickness)  # Top right corner
#     cv2.circle(image, (x1 + 20, y2 - 20), 20, color, thickness)  # Bottom left corner
#     cv2.circle(image, (x2 - 20, y2 - 20), 20, color, thickness)  # Bottom right corner

# def process_image(image):
#     if image.shape[2] == 4:  # Check if the image has an alpha channel
#         image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

#     results = model(image)
    
#     fire_detected = False

#     for result in results:
#         boxes = result.boxes
#         for box in boxes:
#             x1, y1, x2, y2 = map(int, box.xyxy[0])
#             class_id = int(box.cls[0])
#             class_name = model.names[class_id].lower()

#             # Fire detected, draw rounded rectangle
#             fire_detected = True
#             color = (0, 0, 255)  # Red for fire
#             draw_rounded_rectangle(image, (x1, y1), (x2, y2), color, 5)  # Draw rounded rectangle around fire

#             # Draw label
#             label = "Fire Detected"
#             cv2.putText(image, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#     # Trigger alarm if fire is detected
#     if fire_detected:
#         play_alarm()
    
#     return image

# # Function to capture from the laptop camera in real-time
# def run_camera():
#     cap = cv2.VideoCapture(0)  # Access laptop camera
#     stframe = st.empty()  # Placeholder for the video stream

#     while cap.isOpened():
#         ret, frame = cap.read()
#         if not ret:
#             st.write("Camera not working!")
#             break
        
#         annotated_frame = process_image(frame)
        
#         # Display the frame in Streamlit
#         stframe.image(annotated_frame, channels="BGR", use_column_width=True)

#         # Add a small delay to control the frame rate
#         time.sleep(0.03)

# # Streamlit app interface
# st.title("Fire Detection with Alarm System")

# # Start real-time camera feed
# if st.button('Start Camera'):
#     run_camera()

# # Stop alarm when user presses the button
# if st.button('Stop Alarm'):
#     pygame.mixer.music.stop()
