import cv2 
import mediapipe as mp
import csv
import os

import pandas as pd



# import cv2
import numpy as np
# import csv
length_Of_vid = 10


def extract_nmx_from_video(video_name):
    # Split the video name into components using '-' as a delimiter
    video_name_values = video_name.split("-")
    body_part = video_name_values[0]
    recovery_timeline = video_name_values[1]
    intensity = video_name_values[2].split(".")[0]  # Remove file extension from intensity
    return body_part, recovery_timeline, intensity

def generate_header(target_fps=30, duration=10):
    header = []
    
    # Loop through the duration in seconds and frame positions
    for time_seconds in range(duration):
        for frame_position in range(target_fps):
            # Generate headers for pose landmarks
            for i in range(33):  # Assuming 33 pose landmarks from MediaPipe Pose
                header.append(f"{time_seconds:02f}_{frame_position:02f}_pose_{i}_x")
                header.append(f"{time_seconds:02f}_{frame_position:02f}_pose_{i}_y")
                header.append(f"{time_seconds:02f}_{frame_position:02f}_pose_{i}_z")

            # Generate headers for hand landmarks (21 landmarks per hand, 2 hands)
            for hand_index in range(2):  # Assuming up to 2 hands
                for i in range(21):  # Each hand has 21 landmarks
                    header.append(f"{time_seconds:02f}_{frame_position:02f}_hand_{hand_index}_{i}_x")
                    header.append(f"{time_seconds:02f}_{frame_position:02f}_hand_{hand_index}_{i}_y")
                    header.append(f"{time_seconds:02f}_{frame_position:02f}_hand_{hand_index}_{i}_z")

    return header



def process_video(video_path, output_csv, n, m, x, target_fps=30):
    # Initialize mediapipe solutions
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()

    # Initialize video capture
    cap = cv2.VideoCapture(video_path)

    # Get video frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Check if fps is valid
    if fps == 0:
        print("Error: Unable to read video frame rate.")
        return

    # Ensure target_fps is not greater than fps
    if target_fps > fps:
        print(f"Warning: target_fps {target_fps} is greater than the video's fps {fps}. Setting target_fps to {fps}.")
        target_fps = fps

    frame_interval = max(1, int(fps / target_fps))  # Calculate frame interval ensuring it's at least 1

    # Initialize frame count
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process every frame at the interval that matches target FPS
        if frame_count % frame_interval == 0:
            # Calculate the current time in seconds based on frame_count
            time_seconds = frame_count // fps
            frame_position = (frame_count // frame_interval) % target_fps  # Ensure integer

            # Prepare row data with n, m, x, and timestamp/frame info
            row_data = [n, m, x]  # Include n, m, x values at the start of each row

            # Extract pose landmarks and append values
            pose_results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if pose_results.pose_landmarks:
                pose_landmarks = pose_results.pose_landmarks.landmark

                for i, landmark in enumerate(pose_landmarks):
                    # Append corresponding values for pose landmarks
                    row_data.append(landmark.x)
                    row_data.append(landmark.y)
                    row_data.append(landmark.z)

            # Extract hand landmarks and append values
            hand_results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if hand_results.multi_hand_landmarks:
                for hand_index, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        # Append corresponding values for hand landmarks
                        row_data.append(landmark.x)
                        row_data.append(landmark.y)
                        row_data.append(landmark.z)

            # Add timestamp and frame info to row_data
            row_data = [f"{time_seconds:02f}_{frame_position:02f}"] + row_data  # Timestamp at index 0
            row_data.insert(1, frame_position)  # Insert frame position at index 1

            # Open CSV file to write data
            with open(output_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                # Write the row data (n, m, x + landmarks data)
                writer.writerow(row_data)

        # Increment frame count
        frame_count += 1

    # Release video capture
    cap.release()


def main_process_videos(folder_path, output_csv, target_fps=30):
    # Generate the CSV header
    header = generate_header(target_fps)

    # Add the n, m, x columns to the header
    header = ['n', 'm', 'x'] + header

    # Write the header to the CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)

    # Process each video in the folder and append the rows of values
    for file_name in os.listdir(folder_path):
        if file_name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
            video_path = os.path.join(folder_path, file_name)
            # Extract n, m, x from the video filename
            n, m, x = extract_nmx_from_video(file_name)
            # Process the video and append the data to the CSV
            process_video(video_path, output_csv, n, m, x, target_fps)

# Constants for canvas size and landmark scaling
CANVAS_SIZE = (640, 480)
LANDMARK_RADIUS = 5
POSE_COLOR = (0, 255, 0)  # Green for pose
HAND_COLOR = (255, 0, 0)  # Blue for hands

def draw_landmarks(frame, landmarks, color):
    """Draws landmarks on the given frame"""
    for i in range(0, len(landmarks), 3):  # x, y, z come in triples
        x = int(landmarks[i] * CANVAS_SIZE[0])
        y = int(landmarks[i + 1] * CANVAS_SIZE[1])
        # Draw a circle at the landmark position
        cv2.circle(frame, (x, y), LANDMARK_RADIUS, color, -1)

def generate_video_from_landmarks(csv_file, output_video_path, target_fps=30, frame_size=(640, 480)):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Get the total number of frames (rows) in the CSV
    total_frames = len(df)

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Use appropriate codec
    out = cv2.VideoWriter(output_video_path, fourcc, target_fps, frame_size)

    for frame_idx in range(total_frames):
        # Get the row corresponding to the current frame
        row = df.iloc[frame_idx]

        # Extract landmarks data
        landmarks = row[3:].values  # Skip n, m, x columns

        # Create a blank image for the frame
        frame = np.zeros((frame_size[1], frame_size[0], 3), dtype=np.uint8)

        # Draw pose landmarks
        for i in range(33):  # Assuming 33 pose landmarks
            x = int(landmarks[i * 3] * frame_size[0])  # x-coordinate
            y = int(landmarks[i * 3 + 1] * frame_size[1])  # y-coordinate
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)  # Draw pose landmark

        # Draw hand landmarks
        for hand_index in range(2):  # Assuming 2 hands
            for i in range(21):  # Each hand has 21 landmarks
                x = int(landmarks[99 + hand_index * 63 + i * 3] * frame_size[0])  # Hand x-coordinate
                y = int(landmarks[99 + hand_index * 63 + i * 3 + 1] * frame_size[1])  # Hand y-coordinate
                cv2.circle(frame, (x, y), 5, (255, 0, 0), -1)  # Draw hand landmark

        # Write the frame to the video
        out.write(frame)

    # Release the video writer
    out.release()
    print(f"Video saved as: {output_video_path}")

# Example usage
folder_path = 'videos\\'  # Replace with your folder path
output_csv = 'output_landmarks_2.csv'
main_process_videos(folder_path, output_csv)
generate_video_from_landmarks(output_csv,"test_2.mp4")