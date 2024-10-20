import json

# Define the input data
input_data = {
    "pH": 7.5,
    "Hardness": 180.0,
    "Solids": 300.5,
    "Chloramines": 10.2,
    "Sulfate": 220.5,
    "Conductivity": 400.0,
    "Organic_carbon": 8.0,
    "Trihalomethanes": 25.0,
    "Turbidity": 4.5
}

# Define the file path for the JSON file
json_file_path = 'input_data.json'

# Serialize the dictionary to JSON format
json_data = json.dumps(input_data, indent=4)

# Write the JSON data to a file
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f"JSON file '{json_file_path}' created successfully.")
