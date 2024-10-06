import cv2
import mediapipe as mp
import pandas as pd
import csv

# Function to load shoulder coordinates from demo CSV
def load_shoulder_coordinates(demo_csv):
    demo_data = pd.read_csv(demo_csv)
    right_shoulder_x = demo_data[demo_data['time_frame_pose_x'].str.contains('right_shoulder_x')]['time_frame_pose_x'].iloc[0].split('_')[-1]
    right_shoulder_y = demo_data[demo_data['time_frame_pose_x'].str.contains('right_shoulder_y')]['time_frame_pose_x'].iloc[0].split('_')[-1]
    return float(right_shoulder_x), float(right_shoulder_y)

# Process camera input and display landmarks and demo shoulder position
def process_camera_with_demo(output_csv, demo_csv, n, m, x):
    # Load demo shoulder coordinates
    demo_x, demo_y = load_shoulder_coordinates(demo_csv)

    # Initialize mediapipe solutions
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    
    # Initialize video capture
    cap = cv2.VideoCapture(0)  # Use the first camera

    # Open CSV file to write data
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the CSV header
        header = ['n', 'm', 'x', 'time_frame_pose_x']
        writer.writerow(header)

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert the image to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            

            with mp_hands.Hands(static_image_mode= False ) as hands, mp_pose.Pose(static_image_mode=False) as pose:
                pose_results = pose.process(rgb_frame)
                hand_results = hands.process(rgb_frame)
                # Draw landmarks and demo shoulder position
                if pose_results.pose_landmarks:
                    for landmark in pose_results.pose_landmarks.landmark:
                        # Convert landmark coordinates to pixel values
                        h, w, _ = frame.shape
                        x_px = int(landmark.x * w)
                        y_px = int(landmark.y * h)
                        
                        # Draw the live landmarks
                        cv2.circle(frame, (x_px, y_px), 5, (0, 255, 0), -1)  # Green for live landmarks
               # Draw hand landmarks
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        for landmark in hand_landmarks.landmark:
                            # Convert landmark coordinates to pixel values
                            h, w, _ = frame.shape
                            x_px = int(landmark.x * w)
                            y_px = int(landmark.y * h)

                            # Draw the live landmarks
                            cv2.circle(frame, (x_px, y_px), 5, (0, 255, 0), -1)  # Green for hand landmarks

                # for

            # TODO: render the image of the shoulder
            
            # Show the image
            cv2.imshow('Camera Feed', frame)

            # Write data to CSV (optional, depending on your needs)
            # ... (add any additional CSV logging here)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# Example usage
process_camera_with_demo('output_landmarks_camera.csv', 'output_landmarks.csv', 'n_value', 'm_value', 'x_value')