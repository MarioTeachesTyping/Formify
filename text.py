import cv2
import mediapipe as mp

# Initialize MediaPipe pose and hands solutions
mp_pose = mp.solutions.pose
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils  # For drawing the landmarks

# Function to process video and extract landmarks
def extract_landmarks_from_video(video_path, output_dir):
    # Initialize Pose and Hands solutions
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()

    # Capture video
    cap = cv2.VideoCapture(video_path)
    frame_idx = 0
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB (MediaPipe requires RGB input)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame for pose landmarks
        pose_results = pose.process(rgb_frame)

        # Process the frame for hand landmarks
        hands_results = hands.process(rgb_frame)

        # If pose landmarks are detected
        if pose_results.pose_landmarks:
            # Draw pose landmarks on the frame
            mp_drawing.draw_landmarks(frame, pose_results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # If hand landmarks are detected
        if hands_results.multi_hand_landmarks:
            for hand_landmarks in hands_results.multi_hand_landmarks:
                # Draw hand landmarks on the frame
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Save the frame with landmarks
        cv2.imwrite(f"{output_dir}/frame_{frame_idx}.jpg", frame)
        frame_idx += 1

        # Display the frame (optional)
        cv2.imshow('Landmarks', frame)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Path to the input video and output directory for saving landmark frames
video_path = 'videos\\acl_week8_easy.mp4'  # Replace with your video path
output_dir = 'landmark_frames'  # Replace with your desired output folder

# Call the function to extract landmarks from the video
extract_landmarks_from_video(video_path, output_dir)
