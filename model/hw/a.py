import serial
import time
import json

# Configure the serial port
ser = serial.Serial('COM4', 9600)  # Replace 'COM4' with your serial port
time.sleep(2)  # Wait for the serial connection to initialize

try:
    with open('sensor_data.json', 'a') as f:
        while True:
            # Read a line from the serial port
            line = ser.readline().decode('latin-1').strip()

            # Print the received line for debugging
            print("Received:", line)

            # Check if the line contains the correct sensor data format
            if line.startswith('Temperature:'):
                # Extract the sensor values from the line
                parts = line.split(',')
                temperature = float(parts[0].split(': ')[1].replace('°C', ''))
                humidity = float(parts[1].split(': ')[1].replace('%', ''))
                soil_moisture = float(parts[2].split(': ')[1])
                ph_value = float(parts[3].split(': ')[1])

                # Create a dictionary to hold sensor values
                sensor_data = {
                    'temperature': temperature,
                    'humidity': humidity,
                    'soil_moisture': soil_moisture,
                    'ph_value': ph_value
                }

                # Write sensor data to JSON file
                json.dump(sensor_data, f)
                f.write('\n')  # Add newline to separate entries

                # Print the sensor values for verification
                print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Soil Moisture: {soil_moisture}, pH: {ph_value}")

except KeyboardInterrupt:
    print("Exiting...")
finally:
    ser.close()
