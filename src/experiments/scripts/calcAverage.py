import matplotlib.pyplot as plt
import csv
import pandas as pd

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

#average calc
n = len(first_values)
sum = 0
for i in range(n):
    sum = sum + timeWithTelegrafSlow[i]

def mean_squared_error(actual, predicted):
    if len(actual) != len(predicted):
        raise ValueError("Lists must have the same length.")
    mse = sum((a - p) ** 2 for a, p in zip(actual, predicted)) / len(actual)
    return mse

print(max(timeWithTelegrafFast))

#print(mean_squared_error(first_values, second_values))

print(sum/n)