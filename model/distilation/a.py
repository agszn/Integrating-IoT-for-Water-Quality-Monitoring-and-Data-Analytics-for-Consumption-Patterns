# Load modules
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import pandas as pd
import numpy as np  # Import numpy for handling null values

# Pickle model
import pickle

# Unpickle model
model = pd.read_pickle(r'new_model.pickle')
# read a pickle pd.read_pickle('model.pkl')

# Take input from user
# pH: The pH level of the water.
# Hardness: Water hardness, a measure of mineral content.
# Solids: Total dissolved solids in the water.
# Chloramines: Chloramines concentration in the water.
# Sulfate: Sulfate concentration in the water.
# Conductivity: Electrical conductivity of the water.
# Organic_carbon: Organic carbon content in the water.
# Trihalomethanes: Trihalomethanes concentration in the water.
# Turbidity: Turbidity level, a measure of water clarity.
# Potability: Target variable; indicates water potability with values 1 (potable) and 0 (not potable).
pH = 3.71608007538699
Hardness = 129.42292051494425
Solids = 18630.057857970347
Chloramines = 6.635245883862
Sulfate = 0
Conductivity = 592.8853591348523
Organic_carbon = 15.180013116357259
Trihalomethanes = 56.32907628451764
Turbidity = 4.500656274942408

# Handling null values in user input
user_input = np.array([[pH, Hardness, Solids, Chloramines, Sulfate, Conductivity, Organic_carbon, Trihalomethanes,Turbidity]])
user_input = np.nan_to_num(user_input)  # Replace NaN with zero

result = model.predict(user_input)  # input must be 2D array
print(result)

# Print the predicted class
if result == 1:
    print("The water is potable.")
else:
    print("The water is not potable.")