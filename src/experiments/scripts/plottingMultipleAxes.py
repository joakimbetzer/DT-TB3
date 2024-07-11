import matplotlib.pyplot as plt
import csv
import time
import numpy as np

def update_plot():
    # Initialize lists to store the data
    first_values = []
    second_values = []
    third_values = []
    fourth_value = []

    # Open and read the CSV file
    with open('safety.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert the strings to floats and store them
            first_values.append(float(row[0]))
            second_values.append(float(row[1]))
            third_values.append(float(row[2]))
            fourth_value.append(row[3].strip().lower() == 'true')

    # Generate the x values
    x_values = [i * 2 for i in range(len(first_values))]

    # Set the style to a default background
    plt.style.use('default')

    # Create the plot
    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax2 = ax1.twinx()

    # Plot the first values
    points1 = ax1.scatter(x_values, first_values, color='cyan', label='ActualSpeed Points')
    line1, = ax1.plot(x_values, first_values, linestyle='-', color='cyan', alpha=0.5)  # Plot the line but don't include it in the legend

    # Plot the second values with dashed line
    line2, = ax2.plot(x_values, second_values, linestyle='--', color='magenta', alpha=0.5)  # Plot the line but don't include it in the legend

    third_values_ahead = third_values[:27]
    third_values_behind = third_values[28:]

    # Plot the third values with dashed lines
    line3, = ax2.plot(x_values[:27], third_values_ahead, label='Lidar[0] (Front of robot)', linestyle='--', color='green')
    line4, = ax2.plot(x_values[28:], third_values_behind, label='Lidar[179] (Back of robot)', linestyle='--', color='red')

    # Highlight the points based on the fourth column
    safety_triggered_points = []
    braking_distance_points = []
    for x, y, is_optimized in zip(x_values, second_values, fourth_value):  # Change first_values to second_values here
        if is_optimized:
            safety_triggered_points.append(ax2.scatter(x, y, color='red', marker='x'))
        else:
            braking_distance_points.append(ax2.scatter(x, y, color='magenta'))

    # Add labels and title
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Speed')
    ax2.set_ylabel('Distance')

    # Combine legends from both axes
    handles = [points1, line3, line4]
    labels = ['ActualSpeed Points', 'Lidar[0] (Front of robot)', 'Lidar[179] (Back of robot)']

    
    if braking_distance_points:
        handles.append(braking_distance_points[0])
        labels.append('BrakingDistance')

    if safety_triggered_points:
        handles.append(safety_triggered_points[0])
        labels.append('Safety triggered')

    ax1.legend(handles, labels, loc='upper right')

    fig.tight_layout()  # otherwise the right y-label is slightly clipped   

    plt.title('Plot of testing safety runtime monitor with simulated data')

    # Customize the grid and tick marks
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.tick_params(colors='black')

    # Save the plot to a file
    plt.savefig('safety2.png', dpi=300)  # Save as PNG file with high resolution

    # Close the plot to free memory
    plt.close()

# Main loop to update the plot periodically
try:
    while True:
        update_plot()
        time.sleep(3)
except KeyboardInterrupt:
    print("Plot update stopped.")