import cv2
import mediapipe as mp
import csv
import os
import numpy as np

# Constants
DURATION = 10  # Duration of the video in seconds
TARGET_FPS = 28  # Target frames per second
NUM_POSE_LANDMARKS = 33  # Number of pose landmarks
NUM_HAND_LANDMARKS = 21  # Number of landmarks per hand
NUM_HANDS = 2  # Assuming two hands
TOTAL_LANDMARKS = (NUM_POSE_LANDMARKS * 3) + (NUM_HANDS * NUM_HAND_LANDMARKS * 3)  # Total landmarks (x, y, z)

def generate_header():
    """Generates the CSV header based on the number of landmarks and required columns."""
    header = ['timestamp', 'fps', 'm', 'n', 'x']  # Basic columns
    
    # Pose landmark columns
    for i in range(NUM_POSE_LANDMARKS):
        header.append(f'pose_landmark_{i}_x')
        header.append(f'pose_landmark_{i}_y')
        header.append(f'pose_landmark_{i}_z')
    
    # Hand landmark columns (for both hands)
    for hand_index in range(NUM_HANDS):
        for i in range(NUM_HAND_LANDMARKS):
            header.append(f'hand_{hand_index}_landmark_{i}_x')
            header.append(f'hand_{hand_index}_landmark_{i}_y')
            header.append(f'hand_{hand_index}_landmark_{i}_z')
    
    return header

def extract_mnx_from_video(video_name):
    """Extracts n, m, x values from the video filename."""
    video_name_values = video_name.split("-")
    body_part = video_name_values[0]
    recovery_timeline = video_name_values[1]
    intensity = video_name_values[2].split(".")[0]  # Remove file extension
    return recovery_timeline, body_part, intensity

def process_video(video_path, output_csv, n, m, x, target_fps=TARGET_FPS):
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

    target_fps  = fps

    # Initialize frame count
    frame_count = 0

    # Total frames needed for 10 seconds
    total_frames_needed = target_fps * DURATION  # 150 frames for 10 seconds

    # Write the header if the file doesn't exist
    if not os.path.exists(output_csv):
        with open(output_csv, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(generate_header())  # Write header to CSV

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
            row_data = [f"{int(time_seconds)}_{int(frame_position)}",fps, n, m, x]  # Include timestamp and n, m, x values

            # Extract pose landmarks and append values
            pose_results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if pose_results.pose_landmarks:
                pose_landmarks = pose_results.pose_landmarks.landmark

                for i, landmark in enumerate(pose_landmarks):
                    # Append corresponding values for pose landmarks
                    row_data.append(landmark.x)
                    row_data.append(landmark.y)
                    row_data.append(landmark.z)
            else:
                # Append None values for pose landmarks if not detected
                row_data.extend([None, None, None] * NUM_POSE_LANDMARKS)  # Assuming 33 pose landmarks

            # Extract hand landmarks and append values
            hand_results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if hand_results.multi_hand_landmarks:
                for hand_index, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                    for i, landmark in enumerate(hand_landmarks.landmark):
                        # Append corresponding values for hand landmarks
                        row_data.append(landmark.x)
                        row_data.append(landmark.y)
                        row_data.append(landmark.z)
            else:
                # Append None values for hand landmarks if not detected
                row_data.extend([None, None, None] * (NUM_HANDS * NUM_HAND_LANDMARKS))  # Assuming 21 landmarks per hand, 2 hands

            # Write the row data (timestamp, n, m, x + landmarks data) to the CSV
            with open(output_csv, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(row_data)

        # Increment frame count
        frame_count += 1

    # Ensure at least 150 rows are created in the CSV
    while frame_count < total_frames_needed:
        # Write a row with empty landmark data or NaN values
        empty_row = [f"{frame_count // target_fps}_{frame_count % target_fps}",fps,  n, m, x] + [None] * (len(generate_header()) - 4)  # Adjust for your total columns
        with open(output_csv, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(empty_row)
        frame_count += 1

    # Release video capture
    cap.release()

# Example usage
folder_path = 'videos\\'  # Replace with your folder path
output_csv = 'output_landmarks_final.csv'

# Process each video in the folder and generate CSV
for file_name in os.listdir(folder_path):
    if file_name.endswith(('.mp4', '.avi', '.mov', '.mkv')):
        video_path = os.path.join(folder_path, file_name)
        m, n, x = extract_mnx_from_video(file_name)
        process_video(video_path, output_csv, m, n, x)
