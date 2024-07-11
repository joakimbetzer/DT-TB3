#!/usr/bin/env python

import csv
import json
import os
import random
import rospy
import paho.mqtt.client as mqtt
from std_msgs.msg import String
from my_custom_msgs.msg import LidarData

# MQTT Broker Information
broker_address = "test.mosquitto.org"
broker_port = 1883

dataStream = "Data"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    # Initialize MQTT subscriber to "Action" topic
    client.subscribe("Action")
    # Initialize MQTT subscriber to "Data" ROS topic
    rospy.Subscriber(dataStream, LidarData, ros_callback)

def on_action_message(client, userdata, msg):
    print("Received message from DT: ", str(msg.topic))
    print(msg.payload)
    print("\n")
    try:
        #print("published message to ROS: ", msg.payload)
        pub.publish(msg.payload)
    except rospy.exceptions.ROSInitException:
        print("ROS is not running")


# ROS Callback for publishing to MQTT
def ros_callback(data):
    data_to_publish = {
    "int_data": data.lidar_values,
    "str_data": data.additional_data
    }

    message = json.dumps(data_to_publish)
    message_dict = json.loads(message)

    # Extracting data from the received message
    lidar_data = [message_dict["int_data"][0],[message_dict["int_data"][179]]]
    left_wheel_pos = float(message_dict["str_data"][1])
    right_wheel_pos = float(message_dict["str_data"][2])
    left_wheel_vel = float(message_dict["str_data"][3])
    right_wheel_vel = float(message_dict["str_data"][4])
    actual_speed = float(message_dict["str_data"][5])
    linear_x = float(message_dict["str_data"][6])
    angular_z = float(message_dict["str_data"][7])
    brakingDist = actual_speed * 2 #Because frequency of ROS is 2 seconds

    '''
    #For testing validation
    #actual_speed = random.uniform(-0.04,0.26)
    with open("validation.csv", mode='ab') as file:
        writer = csv.writer(file)
        writer.writerow([actual_speed])
    '''

    # Create the final JSON structure
    final_message = {
        "lidar": lidar_data,
        "left_wheel_pos": left_wheel_pos,
        "right_wheel_pos": right_wheel_pos,
        "left_wheel_vel": left_wheel_vel,
        "right_wheel_vel": right_wheel_vel,
        "actualSpeed": actual_speed,
        "expectedSpeed": linear_x,
        "angular_z": angular_z,
        "brakingDist": brakingDist
    }

    # Convert to JSON string
    json_data = json.dumps(final_message)
    client.publish("Data", json_data)

# Initialize publisher for "Action" ROS topic
pub = rospy.Publisher("Action", String, queue_size=1)

# Initialize MQTT Client
client = mqtt.Client()
client.on_connect = on_connect
client.message_callback_add("Action", on_action_message)

# Connect to MQTT Broker
client.connect(broker_address, broker_port, 60)

client.loop_start()

# ROS Node Initialization
rospy.init_node('mqtt_ros_bridge', anonymous=True)

# ROS Spin
rospy.spin()

client.loop_stop()
client.disconnect()