import cv2
import mediapipe as mp
import pandas as pd
import os
import time

# Initialize mediapipe solutions
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Initialize pose and hands models
pose = mp_pose.Pose()
hands = mp_hands.Hands()

# Prepare the CSV file
csv_file_path = 'landmarks_data.csv'
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)  # Remove the file if it already exists

# Initialize DataFrame for storing landmark data
columns = ['n', 'm', 'x', 'time_frame_pose_x']
landmark_data = pd.DataFrame(columns=columns)

# Dummy values for n, m, x
n_value = 'n_value'
m_value = 'm_value'
x_value = 'x_value'

# Start the frame capture loop
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    
    # Flip the frame for a selfie-view display
    frame = cv2.flip(frame, 1)
    
    # Convert the image to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame for pose landmarks
    pose_results = pose.process(rgb_frame)
    
    # Process the frame for hand landmarks
    hand_results = hands.process(rgb_frame)

    # Prepare the current timestamp
    timestamp = time.time()
    
    # Create a temporary DataFrame for this frame's landmarks
    frame_landmarks = pd.DataFrame(columns=columns)

    # Draw pose landmarks
    if pose_results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Extract pose landmarks
        for idx, landmark in enumerate(pose_results.pose_landmarks.landmark):
            # Create the time_frame_pose_x string
            time_frame_pose_x = f"{timestamp}_{idx}_pose_x_{landmark.x}"
            frame_landmarks = pd.concat([frame_landmarks, pd.DataFrame({
                'n': [n_value],
                'm': [m_value],
                'x': [x_value],
                'time_frame_pose_x': [time_frame_pose_x]
            })], ignore_index=True)

            # Append y and z coordinates
            time_frame_pose_y = f"{timestamp}_{idx}_pose_y_{landmark.y}"
            frame_landmarks = pd.concat([frame_landmarks, pd.DataFrame({
                'n': [n_value],
                'm': [m_value],
                'x': [x_value],
                'time_frame_pose_x': [time_frame_pose_y]
            })], ignore_index=True)

            time_frame_pose_z = f"{timestamp}_{idx}_pose_z_{landmark.z}"
            frame_landmarks = pd.concat([frame_landmarks, pd.DataFrame({
                'n': [n_value],
                'm': [m_value],
                'x': [x_value],
                'time_frame_pose_x': [time_frame_pose_z]
            })], ignore_index=True)

    # Draw hand landmarks
    if hand_results.multi_hand_landmarks:
        for hand_landmarks in hand_results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract hand landmarks
            for hand_idx, landmark in enumerate(hand_landmarks.landmark):
                time_frame_hand_x = f"{timestamp}_{hand_idx}_hand_x_{landmark.x}"
                frame_landmarks = pd.concat([frame_landmarks, pd.DataFrame({
                    'n': [n_value],
                    'm': [m_value],
                    'x': [x_value],
                    'time_frame_pose_x': [time_frame_hand_x]
                })], ignore_index=True)

                time_frame_hand_y = f"{timestamp}_{hand_idx}_hand_y_{landmark.y}"
                frame_landmarks = pd.concat([frame_landmarks, pd.DataFrame({
                    'n': [n_value],
                    'm': [m_value],
                    'x': [x_value],
                    'time_frame_pose_x': [time_frame_hand_y]
                })], ignore_index=True)

                time_frame_hand_z = f"{timestamp}_{hand_idx}_hand_z_{landmark.z}"
                frame_landmarks = pd.concat([frame_landmarks, pd.DataFrame({
                    'n': [n_value],
                    'm': [m_value],
                    'x': [x_value],
                    'time_frame_pose_x': [time_frame_hand_z]
                })], ignore_index=True)

    # Append the current frame's landmarks to the main DataFrame
    landmark_data = pd.concat([landmark_data, frame_landmarks], ignore_index=True)

    # Save to CSV file periodically
    landmark_data.to_csv(csv_file_path, index=False)

    # Display the frame
    cv2.imshow('Pose and Hand Landmarks', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()
