import csv

# Function to generate the new index values
def generate_index_values(start, step, num_lines):
    index_values = []
    current_value = start
    for i in range(num_lines):
        if current_value > 0:
            index_values.append(round(current_value, 2))
            current_value -= step
        else:
            index_values.append(0)
    return index_values

# Read the CSV file
input_file = 'dataBackWards.csv'
output_file = 'dataBackWards.csv'


# Read the data from the input file
with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Generate the new index values
num_lines = len(data)
start_value = 0.5
step_value = 0.02
index_values = generate_index_values(start_value, step_value, num_lines)

# Modify the data
for i, line in enumerate(data):
    line[179] = index_values[i]
'''
with open(input_file, mode='r') as file:
    reader = csv.reader(file)
    data = list(reader)

# Modify the data
for line in data:
    if len(line) > 364:  # Ensure the line has enough elements
        line[365] = -float(line[365])
'''

# Write the modified data to the output file
with open(output_file, mode='w') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print("Data has been modified and saved to {}".format(output_file))
