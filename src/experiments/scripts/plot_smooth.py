import matplotlib.pyplot as plt
import csv
import pandas as pd
import time

def update_plot():
    # Initialize lists to store the data
    first_values = []
    second_values = []
    third_values = []

    # Open and read the CSV file
    with open('C.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert the strings to floats and store them
            first_values.append(float(row[0]))
            second_values.append(float(row[1]))
            third_values.append(row[2].strip().lower() == 'true')

    # Generate the x values
    x_values = [i * 2 for i in range(len(first_values))]

    # Convert lists to pandas Series
    first_series = pd.Series(first_values)
    second_series = pd.Series(second_values)

    # Apply moving average
    first_smoothed = first_series.rolling(window=5, min_periods=1).mean()

    # Set the style to a dark background
    plt.style.use('default')

    # Create the plot
    plt.figure(figsize=(12, 6))
    plt.ylim(0, 0.125)

    # Plot the first values
    plt.plot(x_values, first_smoothed, label='ActualSpeed (Smoothed)', linestyle='-', marker='o', color='blue')

    # Plot the second values with dashed line
    plt.plot(x_values, second_values, label='Expected speed', linestyle='--', color='red')

    # Highlight the points based on the third column
    for x, y, is_optimized in zip(x_values, second_values, third_values):
        if is_optimized:
            plt.scatter(x, y, color='orange', label='Expected speed (Optimized)' if 'Expected speed (Optimized)' not in plt.gca().get_legend_handles_labels()[1] else "")
        else:
            plt.scatter(x, y, color='red', label='Expected speed (Non-optimized)' if 'Expected speed (Non-optimized)' not in plt.gca().get_legend_handles_labels()[1] else "")

    # Add labels and title
    plt.xlabel('Time')
    plt.ylabel('Speed')
    plt.title('Plot of ActualSpeed and ExpectedSpeed using gmapping SLAM (Smoothed)')
    plt.legend()

    # Customize the grid and tick marks
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.tick_params(colors='black')

    # Save the plot to a file
    plt.savefig('testYAxis.png', dpi=300)  # Save as PNG file with high resolution

    # Close the plot to free memory
    plt.close()

# Main loop to update the plot periodically
try:
    while True:
        update_plot()
        time.sleep(3)
except KeyboardInterrupt:
    print("Plot update stopped.")
