import matplotlib.pyplot as plt
import csv
import time
import numpy as np

def update_plot():
    # Initialize lists to store the data
    first_values = []
    second_values = []
    third_values = []
    fourth_values = []
    fifth_values = []
    sixth_values = []

    timeWithTelegrafSlow = []
    timeWithTelegrafFast = []
    timeWithoutTelegraf = []

    # Open and read the CSV file
    with open('withoutTelegraf.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            # Convert the strings to floats and store them
            first_values.append(float(row[0]))
            second_values.append(float(row[1]))
            third_values.append(float(row[2]))
            fourth_values.append(float(row[3]))
            fifth_values.append(float(row[4]))
            sixth_values.append(float(row[5]))
    
    for i in range(len(first_values)):
            timeWithoutTelegraf.append(abs(first_values[i]-second_values[i]))

    for i in range(len(first_values)):
            timeWithTelegrafSlow.append(abs(third_values[i]-fourth_values[i]))

    for i in range(len(first_values)):
            timeWithTelegrafFast.append(abs(fifth_values[i]-sixth_values[i]))

    x_values = [i * 6.67 for i in range(len(first_values))]

    # Set the style to a default background
    plt.style.use('default')

    # Create the plot
    plt.figure(figsize=(12, 6))

    # Plot second value
    plt.plot(x_values, timeWithTelegrafSlow, label='Time difference between sent and received message with Telegraf - 0.001s', linestyle='-', color='magenta')
    plt.plot(x_values, timeWithTelegrafFast, label='Time difference between sent and received message with Telegraf - 1s', linestyle='-', color='green')
    #plt.plot(x_values, timeWithoutTelegraf, label='Time difference between sent and received message without Telegraf', linestyle='-', color='cyan')
    # Plotting lower and upper bounds
    #plt.axhline(y=0.22, label='Upper bound', color='red')
    #plt.axhline(y=0.00, label='Lower bound', color='green')

    # Plot the second values with dashed line
    #plt.plot(x_values, second_values, label='BrakingDistance', linestyle='--', color='magenta')

    #third_values_ahead = third_values[:27]
    #third_values_behind = third_values[28:]

    # Plot the third values with dashed line
    #plt.plot(x_values[:27], third_values_ahead, label='Lidar[0] (Front of robot)', linestyle='--', color='green')
    #plt.plot(x_values[28:], third_values_behind, label='Lidar[179] (Back of robot)', linestyle='--', color='red')

    # Highlight the points based on the fourth column
    '''
    for x, y, is_optimized in zip(x_values, first_values, fourth_value):
        if is_optimized:
            plt.scatter(x, y, color='red', marker='x', label='Validation triggered' if 'Validation triggered' not in plt.gca().get_legend_handles_labels()[1] else "")
        else:
            plt.scatter(x, y, color='cyan', label='ActualSpeed' if 'ActualSpeed' not in plt.gca().get_legend_handles_labels()[1] else "")
    '''

    # Add labels and title
    plt.xlabel('Execution time (s)')
    plt.ylabel('Message Latency (s)')
    plt.title('Plot of latency test between send and received message - Comparing Telegraf parameters with no Telegraf')
    

    # Customize the grid and tick marks
    plt.grid(True, color='gray', linestyle='--', linewidth=0.5)
    plt.tick_params(colors='black')
    plt.legend()

    # Save the plot to a file
    plt.savefig('withTelegraf.png', dpi=300)  # Save as PNG file with high resolution

    # Close the plot to free memory
    plt.close()

# Main loop to update the plot periodically
try:
    while True:
        update_plot()
        time.sleep(3)
except KeyboardInterrupt:
    print("Plot update stopped.")
