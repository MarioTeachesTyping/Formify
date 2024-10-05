import cv2
import mediapipe as mp
import csv

def process_video(video_path, output_csv, n, m, x, target_fps=10):
    print(video_path)
    # Initialize mediapipe solutions
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    
    # Initialize video capture
    cap = cv2.VideoCapture(video_path)
    
    # Get video frame rate
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps / target_fps)
    
    # Initialize the pose and hand models
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()

    # Open CSV file to write data
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the CSV header
        header = ['n', 'm', 'x', 'time_frame_pose_x']
        writer.writerow(header)
        
        # Initialize frame count
        frame_count = 0
        time_seconds = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process every frame at the interval that matches 10 FPS
            if frame_count % frame_interval == 0:
                # Convert the image to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process pose and hand landmarks
                pose_results = pose.process(rgb_frame)
                hand_results = hands.process(rgb_frame)
                
                # Calculate the current time in seconds based on frame_count
                time_seconds = frame_count // fps
                
                # Extract pose landmarks and save to CSV
                if pose_results.pose_landmarks:
                    for i, landmark in enumerate(pose_results.pose_landmarks.landmark):
                        writer.writerow([n, m, x, f"{int(time_seconds)}_{int(frame_count % fps)}_pose_x_{landmark.x}"])
                        writer.writerow([n, m, x, f"{int(time_seconds)}_{int(frame_count % fps)}_pose_y_{landmark.y}"])
                        writer.writerow([n, m, x, f"{int(time_seconds)}_{int(frame_count % fps)}_pose_z_{landmark.z}"])
                
                # Extract hand landmarks and save to CSV
                if hand_results.multi_hand_landmarks:
                    for hand_landmarks in hand_results.multi_hand_landmarks:
                        for i, landmark in enumerate(hand_landmarks.landmark):
                            writer.writerow([n, m, x, f"{int(time_seconds)}_{int(frame_count % fps)}_hand_x_{landmark.x}"])
                            writer.writerow([n, m, x, f"{int(time_seconds)}_{int(frame_count % fps)}_hand_y_{landmark.y}"])
                            writer.writerow([n, m, x, f"{int(time_seconds)}_{int(frame_count % fps)}_hand_z_{landmark.z}"])
            
            # Increment frame count
            frame_count += 1

        # Release video capture
        cap.release()

# Example usage:
process_video('videos\\arm_stretch.mp4', 'output_landmarks.csv', 'n_value', 'm_value', 'x_value')
