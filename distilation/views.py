from django.shortcuts import render
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd
import numpy as np  
import pickle
from django.http import HttpResponse

import random
from django.contrib.auth.decorators import login_required
import pandas as pd

from myapp.forms import *
from myapp.models import *

from .forms import *
from .models import *

# Load your model at the beginning (assuming it's in the root of your project)
MODEL_PATH = r'model/distilation/destilation.pickle'
model = pd.read_pickle(MODEL_PATH)
ed = random.randint(13, 14)
Model_json = r'model/distilation/input_data.json'

def predict_potability(request):
    if request.method == 'POST':
        # Retrieve user input from the form
        pH = float(request.POST.get('pH'))
        Hardness = float(request.POST.get('Hardness'))
        Solids = float(request.POST.get('Solids'))
        Chloramines = float(request.POST.get('Chloramines'))
        Sulfate = float(request.POST.get('Sulfate'))
        Conductivity = float(request.POST.get('Conductivity'))
        Organic_carbon = float(request.POST.get('Organic_carbon'))
        Trihalomethanes = float(request.POST.get('Trihalomethanes'))
        Turbidity = float(request.POST.get('Turbidity'))

        # Handling null values in user input
        user_input = np.array([[pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]])
        user_input = np.nan_to_num(user_input)  # Replace NaN with zero
        print("Modified user_input:", user_input)

        # Get the sum of user_input
        sum_of_user_input = np.sum(user_input)
        print("Sum of user_input:", sum_of_user_input)
        # Make prediction
        result = model.predict(user_input)
        useability = ""
        # Format the prediction result
        if result == 1:
            prediction = "The water is potable."
            if sum_of_user_input < 6.5:
                useability = "Drinkable"
            elif 6.5 <= sum_of_user_input <= 8.5:
                useability = "Domestic"
            elif 8.5 < sum_of_user_input <= 10:
                useability = "Agriculture"
            else:
                useability = "Groundwater"
            
        else:
            prediction = "The water is not potable."
        
        # Pass the prediction result to the template
        return render(request, 'distilation_result.html', {
            'prediction': prediction,
            'useability':useability,
            'pH': pH,
            'Hardness': Hardness,
            'Solids': Solids,
            'Chloramines': Chloramines,
            'Sulfate': Sulfate,
            'Conductivity': Conductivity,
            'Organic_carbon': Organic_carbon,
            'Trihalomethanes': Trihalomethanes,
            'Turbidity': Turbidity,
        })

    else: 
        return render(request, 'distilation_predict.html')



import json
import numpy as np
from django.shortcuts import render
def predict_potability_json(request):
    if request.method == 'POST':
        # Define the path to the JSON file
        json_file_path = Model_json

        # Read the JSON file
        with open(json_file_path, 'r') as json_file:
            # Load JSON data from the file
            input_data = json.load(json_file)

        # Extract input features from the dictionary
        pH = ed
        Hardness = float(input_data.get('Hardness'))
        Solids = float(input_data.get('Solids'))
        Chloramines = float(input_data.get('Chloramines'))
        Sulfate = float(input_data.get('Sulfate'))
        Conductivity = float(input_data.get('Conductivity'))
        Organic_carbon = float(input_data.get('Organic_carbon'))
        Trihalomethanes = float(input_data.get('Trihalomethanes'))
        Turbidity = float(input_data.get('Turbidity'))

        # Handling null values in user input
        user_input = np.array([[pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes, Turbidity]])
        user_input = np.nan_to_num(user_input)  # Replace NaN with zero
        print("Modified user_input:", user_input)

        # Get the sum of user_input
        sum_of_user_input = np.sum(user_input)
        print("Sum of user_input:", sum_of_user_input)
        # Make prediction
        result = model.predict(user_input)
        useability = ""
        # Make prediction
        result = model.predict(user_input)

        # Format the prediction result
        
        if result == 1:
            prediction = "The water is potable.✔"
            if sum_of_user_input < 6.5:
                useability = "Drinkable"
            elif 6.5 <= sum_of_user_input <= 8.5:
                useability = "Domestic"
            elif 8.5 < sum_of_user_input <= 10:
                useability = "Agriculture"
            else:
                useability = "Groundwater"
            
        else:
            prediction = "The water is not potable.❌"
        # Pass the prediction result to the template
        return render(request, 'd_hw_r.html', {
            'prediction': prediction,
            'pH': pH,
            'Hardness': Hardness,
            'Solids': Solids,
            'Chloramines': Chloramines,
            'Sulfate': Sulfate,
            'Conductivity': Conductivity,
            'Organic_carbon': Organic_carbon,
            'Trihalomethanes': Trihalomethanes,
            'Turbidity': Turbidity,
        })

    else:
        return render(request, 'd_hw.html')

from django.http import JsonResponse

def upload_json(request):
    if request.method == 'POST':
        form = JSONUploadForm(request.POST, request.FILES)
        if form.is_valid():
            json_file = request.FILES['json_file']
            # Process the uploaded JSON file
            # For example, you can read the file content using json.load() and perform further actions
            return render(request, 'd_hw.html')
        else:
            return JsonResponse({'error': 'Invalid form'}, status=400)
    else:
        form = JSONUploadForm()
    return render(request, 'upload.html', {'form': form})


import serial
def read_sensor_data(request):
    if request.method == 'GET':
        # Serial port configuration
        ser = serial.Serial('COM4', 9600)  # Replace 'COM4' with your serial port
        ser.flushInput()

        try:
            sensor_data_list = []
            recommendations = []  # Initialize list to store recommendations

            while True:
                # Read a line from the serial port
                try:
                    line = ser.readline().decode('latin-1').strip()
                except UnicodeDecodeError as e:
                    print("Error decoding line:", e)
                    continue  # Skip processing this line
                
                sensor_data_list.append(line)
 
                # Limit the number of sensor data to be sent to the frontend for demonstration
                if len(sensor_data_list) >= 20:
                    break
                    
            
            return render(request, 'sensor_data.html', {'sensor_data_list': sensor_data_list})
                    
        except KeyboardInterrupt:
            print("Interrupted. Exiting...")
        finally:
            ser.close()
    
    return render(request, 'sensor_data.html', {'error': 'Invalid request method.'})

import serial
def read_sensor_data(request):
    if request.method == 'GET':
        # Serial port configuration
        ser = serial.Serial('COM3', 9600)  # Replace 'COM4' with your serial port
        ser.flushInput()

        try:
            sensor_data_list = []
            recommendations = []  # Initialize list to store recommendations

            while True:
                # Read a line from the serial port
                try:
                    line = ser.readline().decode('latin-1').strip()
                except UnicodeDecodeError as e:
                    print("Error decoding line:", e)
                    continue  # Skip processing this line
                
                sensor_data_list.append(line)
 
                # Limit the number of sensor data to be sent to the frontend for demonstration
                if len(sensor_data_list) >= 20:
                    break
                    
            
            return render(request, 'sensor_data.html', {'sensor_data_list': sensor_data_list})
                    
        except KeyboardInterrupt:
            print("Interrupted. Exiting...")
        finally:
            ser.close()
    
    return render(request, 'sensor_data.html', {'error': 'Invalid request method.'})