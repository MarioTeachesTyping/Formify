import cv2
import pandas as pd
import numpy as np
import os

def generate_images_from_landmarks(csv_path, output_folder, n, m, x, image_size=(640, 480), fps=10):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Read the CSV file
    df = pd.read_csv(csv_path)

    # Filter the dataframe by 'n', 'm', 'x'
    df_filtered = df[(df['n'] == n) & (df['m'] == m) & (df['x'] == x)]

    # Extract the unique time_frame_pose_x values to group frames by time and frame index
    frames = df_filtered['time_frame_pose_x'].unique()

    # Iterate over the unique frames, ensuring we only process 10 frames per second
    for frame_index, frame in enumerate(frames):
        # Create a blank black image
        img = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)

        # Filter data for the current frame
        current_frame_data = df_filtered[df_filtered['time_frame_pose_x'] == frame]
        
        # Draw pose and hand landmarks on the image
        for _, row in current_frame_data.iterrows():
            # Parse time, frame, and coordinate details from 'time_frame_pose_x'
            pose_info = row['time_frame_pose_x'].split('_')
            coord_type = pose_info[-1]  # x, y, z
            body_part = pose_info[2]  # pose or hand
            
            # Skip z-coordinate as we're only plotting x and y
            if coord_type == 'z':
                continue
            
            # Get the corresponding coordinates
            coord_x = row['x'] if coord_type == 'x' else None
            coord_y = row['x'] if coord_type == 'y' else None
            
            if coord_x is not None and coord_y is not None:
                # Scale the coordinates to fit the image size
                coord_x = int(float(coord_x) * image_size[0])
                coord_y = int(float(coord_y) * image_size[1])
                
                # Draw circles to represent the landmarks (pose: green, hand: red)
                color = (0, 255, 0) if body_part == 'pose' else (0, 0, 255)
                cv2.circle(img, (coord_x, coord_y), 5, color, -1)
        
        # Save the current image as an image file (e.g., frame_001.png)
        output_image_path = os.path.join(output_folder, f"frame_{frame_index:03d}.png")
        cv2.imwrite(output_image_path, img)

# Example usage:
generate_images_from_landmarks('output_landmarks.csv', 'landmark_images', 'n_value', 'm_value', 'x_value')
