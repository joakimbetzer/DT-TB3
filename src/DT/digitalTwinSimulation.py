import json
import threading
import paho.mqtt.client as mqtt

import DT

# MQTT broker details
mqtt_broker = "test.mosquitto.org"
mqtt_port = 1883 
rate = None
messages = []

# Callback function for connection
def on_connect(client, userdata, flags, rc):
    client.subscribe("optimization")
    client.subscribe("safety")
    client.subscribe("validation")
    client.subscribe("Data")

    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect to MQTT broker with error code: " + str(rc))

# Callback function for receiving messages
def on_message_data(client, userdata, msg):
    global messages
    try:
        data = json.loads(msg.payload)

        name = data["name"]
        field = data["fields"]["value"]
        message = {"name": name, "field": field}

        messages.append(message)

        if len(messages) <= 2:
            return
        
        for i in messages:
            name = i["name"]
            if name == "validation":
                print(i)
                # Initiating a stop
                if not i["field"]:
                    publish_to_mqtt("Action", "0.0, 0.0")
                    return

        for i in messages:
            name = i["name"]
            if name == "safety":
                print(i)
                # Initiating a stop
                if not i["field"]:
                    publish_to_mqtt("Action", "0.0, 0.0")
                    return
        
        for i in messages:
            name = i["name"]
            # Send back speed, either the same or optimized
            if name == "optimization":
                print(i)
                publish_to_mqtt("Action", str(i["field"]) + ", 0.0")
                return
        
        messages = []

    except (IndexError, ValueError, KeyError):
        if IndexError:
            print("Not a normal message received, IndexError")
            pass
        elif ValueError:
            print("Not a normal message received, ValueError")
            pass
        elif KeyError:
            print("Not a normal message received, KeyError")
            pass

def on_data_tb3(client, userdata, msg):
    data = json.loads(msg.payload)
    DT.makeModel(data["right_wheel_pos"], data["left_wheel_pos"],
                 data["right_wheel_vel"], data["left_wheel_vel"])

# Publishing to MQTT topic
def publish_to_mqtt(topic, message):
    global messages
    messages = []
    client.publish(topic, message)

try:
    # Create MQTT client instance
    client = mqtt.Client()

    # Set up callback functions
    client.on_connect = on_connect
    client.message_callback_add("safety", on_message_data)
    client.message_callback_add("validation", on_message_data)
    client.message_callback_add("optimization", on_message_data)
    client.message_callback_add("Data", on_data_tb3)

    # Connect to MQTT broker
    client.connect(mqtt_broker, mqtt_port, 60)
    client.loop_forever()

    while True:
        pass

# Main thread for user input
except KeyboardInterrupt:
    print("\nKeyboardInterrupt received")
    client.disconnect()