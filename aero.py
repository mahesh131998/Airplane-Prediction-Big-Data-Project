# Import statements
import warnings
warnings.filterwarnings("ignore")
from joblib import load
import pandas as pd
import numpy as np

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# function which performs prediction of delay
def cal_prob(DayofMonth, CRSDepTime, CRSArrTime, Airplane_Name, Arrival, Departure):
    
    # Load trained models using joblib
    airline_encoder = load('airline_encoder.joblib') 
    arr_encoder = load('arr_encoder.joblib')
    dest_encoder = load('dest_encoder.joblib')
    scaler = load('scaler.joblib') 
    svm = load('svm.joblib') 

    # Converting categorical variables using trained encoders

    # Encoding Airline names
    Airplane_Name = np.array(Airplane_Name)
    Airplane_Name = Airplane_Name.reshape(-1, 1)
    A_name = airline_encoder.transform(Airplane_Name)

    # Encoding Arrival airport names
    Arrival = np.array(Arrival)
    Arrival = Arrival.reshape(-1, 1)
    Arr_airport = arr_encoder.transform(Arrival)

    # Encoding Departure airport names
    Departure = np.array(Departure)
    Departure = Departure.reshape(-1, 1)
    Dest_airport = dest_encoder.transform(Departure)

    # Converting input to format accpeted by classifier
    test_case = np.array([DayofMonth,CRSDepTime,CRSArrTime,A_name,Arr_airport,Dest_airport])
    test_case = test_case.reshape(1, -1)
    
    # Performing scaling on data using trained standard scaler
    test_scaled = scaler.transform(test_case)

    # Performing prediction of delay using SVM
    test_svm_pred = svm.predict_proba(test_scaled)
    
    # Converting classifier output to format expected by server. 
    delay_percent = round(test_svm_pred[0][1]*100,3)
    return delay_percent