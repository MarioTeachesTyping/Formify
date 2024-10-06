import cv2
import mediapipe as mp
import numpy as np
import pandas as pd

# Constants
CANVAS_SIZE = (640, 480)
LANDMARK_RADIUS = 5
POSE_COLOR = (0, 255, 0)  # Green for pose
HAND_COLOR = (255, 0, 0)  # Blue for hands
COUNTDOWN_START = 0  # Countdown starting value
TARGET_FPS = 28  # Frame rate




def find_val(matching_row, column_name):
    return matching_row[column_name].values[0]

def vibrate(part, boolean, bdy_type):
    # type represents hand or pose
    print(f"vibrating: {boolean} of {part} at {bdy_type}")

def draw_landmarks(output_csv, frame, pose_landmarks, hand_landmarks, m,n, intensity, countdown_time,  frame_count):
    """Draws pose and hand landmarks on the frame.""" # [column_name].values[0]
    matching_row_data = find_hand_landmark( output_csv, m, n, intensity, countdown_time, frame_count)
    # Draw pose landmarks
    if pose_landmarks:
        for i, landmark in enumerate(pose_landmarks):
            x = int(landmark.x * frame.shape[1])
            y = int(landmark.y * frame.shape[0])
            
            # Retrieve pose landmark values from CSV
            pose_landmark_value_x = find_val( matching_row_data, f'pose_landmark_{i}_x')
            pose_landmark_value_y = find_val( matching_row_data, f'pose_landmark_{i}_y' )

            if(pose_landmark_value_x - x > 0.5 or pose_landmark_value_y > 0.5 or pose_landmark_value_x - x < -0.5 or pose_landmark_value_y < -0.5):
                vibrate(i, True, "pose")
            else:
                vibrate(i, False, "pose")

            cv2.circle(frame, (x, y), LANDMARK_RADIUS, POSE_COLOR, -1)

    # Draw hand landmarks
    if hand_landmarks:
        for hand_index, hand in enumerate(hand_landmarks):
            for j, landmark in enumerate(hand.landmark):
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                 
                # Retrieve hand landmark values from CSV
                hand_landmark_value_x = find_val( matching_row_data, f'hand_{hand_index}_landmark_{j}_x')
                hand_landmark_value_y = find_val( matching_row_data, f'hand_{hand_index}_landmark_{j}_y')

                if(hand_landmark_value_x - x > 0.5 or hand_landmark_value_y > 0.5 or hand_landmark_value_x - x < -0.5 or hand_landmark_value_y < -0.5):
                    vibrate(j, True, "hand")
                else:
                    vibrate(j, False, "hand")

                cv2.circle(frame, (x, y), LANDMARK_RADIUS, HAND_COLOR, -1)
   

# Constants
LANDMARK_RADIUS = 5  # Radius for drawing landmarks
EXPECTED_POSE_COLOR = (255, 255, 0)  # Color for pose landmarks (Green)
EXPECTED_HAND_COLOR = (255, 255, 0)  # Color for hand landmarks (Red)

def draw_expected_landmarks(frame, pose_landmarks, hand_landmarks):
    """Draws pose and hand landmarks on the frame."""
    # Draw pose landmarks
    if pose_landmarks:
        for landmark in pose_landmarks:
            if isinstance(landmark[0], (int, float)) and isinstance(landmark[1], (int, float)):  # Check if coordinates are numbers
                x = int(landmark[0] * frame.shape[1])  # x coordinate
                y = int(landmark[1] * frame.shape[0])  # y coordinate
                cv2.circle(frame, (x, y), LANDMARK_RADIUS, EXPECTED_POSE_COLOR, -1)

    # Draw hand landmarks
    if hand_landmarks:
        for hand in hand_landmarks:
            for landmark in hand:
                if isinstance(landmark[0], (int, float)) and isinstance(landmark[1], (int, float)):  # Check if coordinates are numbers
                    x = int(landmark[0] * frame.shape[1])  # x coordinate
                    y = int(landmark[1] * frame.shape[0])  # y coordinate
                    cv2.circle(frame, (x, y), LANDMARK_RADIUS, EXPECTED_HAND_COLOR, -1)
def generate_time_frame(number_1, number_2):
    """
    Generates a string in the format "X.Y_Z", where:
    - X is the value of number_1
    - Y is the value of number_2
    """
    
    # Format the string
    result = f"{number_1}.0_{number_2}"
    return result

def find_hand_landmark(csv_file, m, n, x, timestamp, frame_position):
    """Returns the specified column from the CSV based on the given m, n, x, timestamp, and frame_position."""
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Calculate the expected timestamp based on the given frame position
    expected_timestamp = generate_time_frame(timestamp, frame_position)

    # Find the row with matching m, n, x values and matching timestamp
    matching_row = df[
        (df['m'] == m) & 
        (df['n'] == n) & 
        (df['x'] == x) & 
        (df['timestamp'] == expected_timestamp)
    ]

    # Check if a matching row is found
    if matching_row.empty:
        print("No matching landmarks found.")
        return None

    # Return the value from the specified column
    return matching_row


def render_landmarks_from_csv(csv_file, frame, m, n, x, timestamp, frame_position):
    """Renders landmarks from CSV based on the given m, n, x, timestamp, and frame_position."""
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Calculate the frame based on timestamp and TARGET_FPS
    # expected_frame = timestamp * TARGET_FPS + frame_position

    # Find rows with any matching m, n, x values and matching frame position
    matching_rows = df[
        (df['m'] == m) & 
        (df['n'] == n) & 
        (df['x'] == x) & 
        (df['timestamp'] == generate_time_frame(timestamp, frame_position))  # Match frame based on calculated index
    ]

    if matching_rows.empty:
        print(f"No landmarks found for m={m}, n={n}, x={x}, timestamp={timestamp}, and frame {frame_position}.")
        return

    # Extract pose landmarks
    pose_landmarks = []
    for _, row in matching_rows.iterrows():
        for i in range(33):  # Assuming 33 pose landmarks
            pose_landmarks.append(
                [row[f'pose_landmark_{i}_x'], row[f'pose_landmark_{i}_y']]  # Only x and y coordinates for pose landmarks
            )

    # Extract hand landmarks
    hand_landmarks = []
    for _, row in matching_rows.iterrows():
        hands = []
        for hand_index in range(2):  # Assuming two hands
            hand = []
            for i in range(21):  # Assuming 21 landmarks per hand
                try:
                    hand.append(
                        [float(row[f'hand_{hand_index}_landmark_{i}_x']), 
                         float(row[f'hand_{hand_index}_landmark_{i}_y'])]  # Only x and y coordinates for hand landmarks
                        # ]
                    )
                except ValueError:
                    print(f"Error converting hand landmark values to float for hand index {hand_index}, landmark index {i}. Row data: {row}")
            hands.append(hand)
        hand_landmarks.append(hands)

    # Draw landmarks on the frame
    draw_expected_landmarks(frame, pose_landmarks, hand_landmarks)



def process_camera(m,n,x,target_fps=TARGET_FPS):
    # Initialize mediapipe solutions
    mp_pose = mp.solutions.pose
    mp_hands = mp.solutions.hands
    pose = mp_pose.Pose()
    hands = mp_hands.Hands()

    # Initialize video capture from the camera
    cap = cv2.VideoCapture(0)  # Use 0 for the default camera

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    # Initialize frame count and countdown time
    frame_count = 0
    countdown_time = COUNTDOWN_START
    # pre

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Extract pose landmarks
        pose_results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        pose_landmarks = pose_results.pose_landmarks.landmark if pose_results.pose_landmarks else []

        # Extract hand landmarks
        hand_results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        hand_landmarks = hand_results.multi_hand_landmarks if hand_results.multi_hand_landmarks else []

      

        # Draw countdown timer and frame count on the frame
        # cv2.putText(frame, f"Countdown: {countdown_time}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, f"Frame: {frame_count}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)



        # Decrement countdown every second
        if frame_count % target_fps == 0:
            countdown_time += 1
            frame_count = 0

        # Reset countdown when it reaches 0
        if countdown_time > 10:
            countdown_time = COUNTDOWN_START
            


        
        # TODO check the landmark here
        # Render the landmark here too 
        render_landmarks_from_csv("output_landmarks_final.csv", frame, m,n,x,countdown_time,frame_count)
          # Draw landmarks on the frame output_csv, frame, pose_landmarks, hand_landmarks, m,n, intensity, countdown_time,  frame_count
        draw_landmarks("output_landmarks_final.csv", frame, pose_landmarks, hand_landmarks,  m,n,x,countdown_time,frame_count)

        # Display the frame with landmarks and countdown
        cv2.imshow("Camera Feed with Landmarks and Countdown", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Increment frame count
        frame_count += 1

    # Release video capture and close windows
    cap.release()
    cv2.destroyAllWindows()




# Main Usage
process_camera("2_3_weeks","leon","easy")
