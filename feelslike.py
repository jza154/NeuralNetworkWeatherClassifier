import glob 
import pandas as pd
import numpy as np
import os.path
import scipy
import re
from os import listdir
from os.path import isfile, join
from scipy import misc
import os.path
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import sys
from pykalman import KalmanFilter


columns = ['Temp (°C)', 'Dew Point Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)']

def getWeatherForTemp():
    global weatherAttributes
    dateparse = lambda x: pd.datetime.strptime(x, '%Y-%m-%d %H:%M:%S')
    path = r'weather_train_set'
    all_rec = glob.iglob(os.path.join(path, "*.csv"), recursive=True)     
    dataframes = (pd.read_csv(f,skiprows=range(0, 16)) for f in all_rec)
    weather_data = pd.concat(dataframes, ignore_index=True)
    weather_data = weather_data[(weather_data["Data Quality"] == "‡")]
    weatherAttributes=weather_data.drop(weather_data.columns[[1, 2, 3, 4,5,7,9,11,12,13,15,16,17,18,19,20,21,22,23,24]], axis=1)
    weatherAttributes['Temp (°C)'] = weatherAttributes['Temp (°C)'].shift(-1)
    weatherAttributes['Date/Time'] = pd.to_datetime(weatherAttributes['Date/Time'])
    weatherAttributes=weatherAttributes[:-1] 
    
def getWeatherForTemp2():
    global weatherAttributes2
    path = r'weather_test_set'
    all_rec = glob.iglob(os.path.join(path, "*.csv"), recursive=True)     
    dataframes = (pd.read_csv(f,skiprows=range(0, 16)) for f in all_rec)
    weather_data = pd.concat(dataframes, ignore_index=True)
    weather_data = weather_data[(weather_data["Data Quality"] == "‡")]
    weatherAttributes2=weather_data.drop(weather_data.columns[[1, 2, 3, 4,5,7,9,11,12,13,15,16,17,18,19,20,21,22,23,24]], axis=1)
    weatherAttributes2['Date/Time'] = pd.to_datetime(weatherAttributes2['Date/Time'])
    weatherAttributes2['Temp (°C)'] = weatherAttributes2['Temp (°C)'].shift(-1) 
    weatherAttributes2=weatherAttributes2[:-1] 
        
def get_data():
    weatherAttributes['Feels Like (°C)'] = weatherAttributes['Temp (°C)'].shift(-1).fillna(30).astype(int)  # TODO: fill in the to-be-predicted temperature
    return weatherAttributes, weatherAttributes[columns].values, weatherAttributes['Feels Like (°C)'].values
 
def get_data2():
    weatherAttributes2['Feels Like (°C)'] = weatherAttributes2['Temp (°C)'].shift(-1).fillna(30).astype(int)  # TODO: fill in the to-be-predicted temperature
    return weatherAttributes2, weatherAttributes2[columns].values, weatherAttributes2['Feels Like (°C)'].values
 
def get_trained_coefficients():
    """
    Create and train a model based on the training_data_file data.

    Return the model, and the list of coefficients for the 'columns' variables in the regression.
    """
    _, X_train, y_train = get_data()
    model = LinearRegression(fit_intercept=True)
    model.fit(X_train, y_train)
    global coef
    coef= model.coef_
    return model, model.coef_

def output_regression(coefficients):
    """
    Print a human-readable summary of the regression results.
    """
    regress = ' + '.join('%.3g*%s' % (coef, col) for col, coef in zip(columns, coefficients))
    print('Feels Like (°C) = ' + regress)

def plot_errors(model):
    """
    Create a histogram of the residuals after the regression.
    """
    _, X_test, y_test = get_data2()
    plt.hist(model.predict(X_test) - y_test, bins=100)
    plt.xlabel('Temp (°C)')
    plt.ylabel('Frequency')
    plt.title('Residual error after using Regression ')
    #plt.savefig('test_errors.png')
    #plt.show()


def smooth_test(coef):
    """
    Do a Kalman filter on the test data, using the prediction derived from the regression.
    """
    weatherAttributes, X_test, _ = get_data2()
    transition_stddev = 1.5
    observation_stddev = 4
    dims = X_test.shape[-1]
    kalman_data = X_test
    initial = X_test[0]
    observation_covariance = np.diag([observation_stddev, 2, 10, 1]) ** 2
    transition_covariance = np.diag([transition_stddev, 80, 100, 10]) ** 2
    transition = np.diag(coef) # transition = identity for all variables

    # TODO: update transition matrix, using coef to predict the temperature

    kf = KalmanFilter(
        initial_state_mean=initial,
        initial_state_covariance=observation_covariance,
        observation_covariance=observation_covariance,
        transition_covariance=transition_covariance,
        transition_matrices=transition,
    )
    kalman_smoothed, _ = kf.smooth(kalman_data)
    
    plt.figure(figsize=(12, 4))
    plt.plot(weatherAttributes['Date/Time'], weatherAttributes['Temp (°C)'], 'b.', alpha=0.5, label='Temperature (°C)')
    plt.plot(weatherAttributes['Date/Time'], kalman_smoothed[:, 0], 'g-', label='Feels Like (°C)')
    plt.xlabel('Dates')
    plt.ylabel('Temp (°C)')
    plt.title('Filter on Temp(°C) using Regression ')
    plt.legend()
    plt.savefig('smoothed.png')
    #plt.show()

def main(): 
    
    getWeatherForTemp()  
    getWeatherForTemp2()
    model, coefficients = get_trained_coefficients()
    output_regression(coefficients)
    smooth_test(coefficients)
    plot_errors(model)
 
if __name__ == "__main__":
    main()
