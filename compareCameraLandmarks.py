import math
import cv2
import mediapipe as mp
import csv

def is_within_radius(point_x, point_y, target_x, target_y, b):
    """Checks if a point (point_x, point_y) is within the radius `b` of the target point (target_x, target_y)."""
    distance = math.sqrt((point_x - target_x)**2 + (point_y - target_y)**2)
    return distance <= b

def read_target_landmarks(output_csv, n, m, x):
    """Reads the target landmarks from the CSV for the specific n, m, x combination."""
    with open(output_csv, mode='r') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Read the header row
        for row in reader:
            # Assume the CSV row starts with the values n, m, x in the first three columns
            if row[0] == n and row[1] == m and row[2] == x:
                return headers, row
    print(f"Error: No matching n, m, x values found in {output_csv}")
    return None, None

def draw_landmarks(frame, landmarks, color):
    """Draws landmarks on the frame using the specified color."""
    for landmark in landmarks:
        # Get the coordinates of the landmark
        x = int(landmark.x * frame.shape[1])
        y = int(landmark.y * frame.shape[0])
        # Draw the landmark as a circle
        cv2.circle(frame, (x, y), 5, color, -1)  # -1 fills the circle

def process_camera_feed_with_comparison(output_csv, n, m, x, b, target_fps=30):
    """Processes the camera feed and compares landmarks with values from the CSV."""
    # Initialize mediapipe solutions
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()

    # Get target data from CSV based on n, m, x combination
    headers, target_data = read_target_landmarks(output_csv, n, m, x)
    if not target_data:
        return  # Exit if no matching data found

    # Initialize video capture (camera feed)
    cap = cv2.VideoCapture(0)  # 0 means using the default camera

    # Get frame rate of the camera
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        print("Error: Unable to read camera frame rate.")
        return

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

            # Extract pose landmarks from camera feed
            pose_results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if pose_results.pose_landmarks:
                user_pose_landmarks = pose_results.pose_landmarks.landmark
                # Draw user's pose landmarks in orange
                draw_landmarks(frame, user_pose_landmarks, (0, 165, 255))  # Orange color

                for i, landmark in enumerate(user_pose_landmarks):
                    # Extract corresponding target data from CSV for the current joint
                    try:
                        # Find target x, y for the user's pose landmarks from the CSV
                        target_x = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_pose_{i}_x")])
                        target_y = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_pose_{i}_y")])

                        # Check if the current pose point is within the radius `b` of the target point
                        if not is_within_radius(landmark.x, landmark.y, target_x, target_y, b):
                            print(f"Pose landmark {i} at frame {frame_count % target_fps:02d} is outside radius")
                    except (ValueError, IndexError):
                        print(f"Pose landmark {i} does not exist in CSV for time {time_seconds} and frame {frame_count % target_fps:02d}")

            # Extract hand landmarks from camera feed
            hand_results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if hand_results.multi_hand_landmarks:
                for hand_index, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                    user_hand_landmarks = hand_landmarks.landmark
                    # Draw user's hand landmarks in yellow
                    draw_landmarks(frame, user_hand_landmarks, (0, 255, 255))  # Yellow color

                    for i, landmark in enumerate(user_hand_landmarks):
                        try:
                            # Find target x, y for the user's hand landmarks from the CSV
                            target_x = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_hand_{hand_index}_{i}_x")])
                            target_y = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_hand_{hand_index}_{i}_y")])

                            # Check if the current hand point is within the radius `b` of the target point
                            if not is_within_radius(landmark.x, landmark.y, target_x, target_y, b):
                                print(f"Hand landmark {i} (hand {hand_index}) at frame {frame_count % target_fps:02d} is outside radius")
                        except (ValueError, IndexError):
                            print(f"Hand landmark {i} does not exist in CSV for time {time_seconds} and frame {frame_count % target_fps:02d}")

            # Draw target landmarks from CSV
            for i in range(len(target_data) // 3):  # Assuming target_data has x, y, z for each landmark
                try:
                    # Draw target pose landmarks in blue
                    target_x = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_pose_{i}_x")])
                    target_y = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_pose_{i}_y")])
                    cv2.circle(frame, (int(target_x * frame.shape[1]), int(target_y * frame.shape[0])), 5, (255, 0, 0), -1)  # Blue color for pose

                    # Draw target hand landmarks in green
                    target_x = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_hand_0_{i}_x")])
                    target_y = float(target_data[headers.index(f"{time_seconds:02d}_{frame_count % target_fps:02d}_hand_0_{i}_y")])
                    cv2.circle(frame, (int(target_x * frame.shape[1]), int(target_y * frame.shape[0])), 5, (0, 255, 0), -1)  # Green color for hand

                except (ValueError, IndexError):
                    continue

        # Display the frame with landmarks
        cv2.imshow('Camera Feed', frame)

        # Exit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Increment frame count
        frame_count += 1

    # Release camera capture and close any open windows
    cap.release()
    cv2.destroyAllWindows()



# Example usage:
process_camera_feed_with_comparison('output_landmarks.csv', 'arm_stretch', '8_12_weeks', 'easy', b=0.02)
