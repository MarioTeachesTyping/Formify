import pandas as pd

def get_left_shoulder_coordinates(csv_file):
    # Read the CSV file
    data = pd.read_csv(csv_file)
    
    # Initialize coordinates
    left_shoulder_coordinates = {'x': None, 'y': None, 'z': None}
    
    # Iterate through the DataFrame to find left shoulder coordinates
    for index, row in data.iterrows():
        if 'left_shoulder_x' in row['time_frame_pose_x']:
            left_shoulder_coordinates['x'] = row['time_frame_pose_x'].split('_')[-1]
        elif 'left_shoulder_y' in row['time_frame_pose_x']:
            left_shoulder_coordinates['y'] = row['time_frame_pose_x'].split('_')[-1]
        elif 'left_shoulder_z' in row['time_frame_pose_x']:
            left_shoulder_coordinates['z'] = row['time_frame_pose_x'].split('_')[-1]
    
    return left_shoulder_coordinates

# Example usage
csv_file_path = 'output_landmarks.csv'
coordinates = get_left_shoulder_coordinates(csv_file_path)
print(f"Left Shoulder Coordinates: {coordinates}")
