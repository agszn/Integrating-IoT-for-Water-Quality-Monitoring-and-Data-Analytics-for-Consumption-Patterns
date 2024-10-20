import serial
import json

# Serial port configuration
ser = serial.Serial('COM3', 9600)  # Replace 'COM4' with your serial port
ser.flushInput()

try:
    with open('sensor_data.json', 'a') as f:
        while True:
            # Read a line from the serial port
            try:
                line = ser.readline().decode('latin-1').strip()
            except UnicodeDecodeError as e:
                print("Error decoding line:", e)
                continue  # Skip processing this line
            
            # Parse the JSON data
            try:
                sensor_data = json.loads(line)
                
                # Write sensor data to JSON file
                json.dump(sensor_data, f)
                f.write('\n')  # Add newline to separate entries
                
                # Print received data for verification
                print("Received sensor data:", sensor_data)
            except json.decoder.JSONDecodeError as e:
                print("Error decoding JSON:", e)
                print("Received data:", line)
                
except KeyboardInterrupt:
    print("Interrupted. Exiting...")
finally:
    ser.close()
