import glob 
import pandas as pd
import numpy as np
import os.path
import scipy
import re
import glob
from PIL import Image
from os import listdir
from os.path import isfile, join
from scipy import misc
import os.path
from skimage import io
from skimage import color
from scipy.misc import imread



image_source="katkam-scaled/"
uncropped_destination_source= "uncropped_images/"
new_destination_source='new_images/'

#Reading CSV Weather Data
def getWeather():
    #adapted from https://stackoverflow.com/questions/20906474/import-multiple-csv-files-into-pandas-and-concatenate-into-one-dataframe
    #read csv and merge them in one dataframe
    path = r'weather'
    all_rec = glob.iglob(os.path.join(path, "*.csv"), recursive=True)     
    dataframes = (pd.read_csv(f,skiprows=range(0, 16)) for f in all_rec)
    weather_data = pd.concat(dataframes, ignore_index=True)
    
    #cleaning data
    #drop NA values and data quality values which are bad
    weather_data = weather_data[(weather_data["Data Quality"] == "‡")]
    weather_data = weather_data.dropna(subset=['Weather'], how='any')
    weather_data = weather_data.rename(columns={'Date/Time': 'date'})
    #drop not needed columns
    # dew point is 8 humidity is 10 wind direction is 12 wind speed is 14
    global weatherAttributes
    weatherAttributes=weather_data.drop(weather_data.columns[[1, 2, 3, 4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]], axis=1)
    weatherAttributes["Weather"] = weatherAttributes["Weather"]

def editLabel(weather):
    if 'Clear' in weather:
        return "Clear"
    elif 'Cloudy' in weather:
        return "Cloudy"
    elif 'Drizzle' in weather:
        return "Rain"
    elif 'Drizzle,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Fog' in weather:
        return "Cloudy"
    elif 'Freezing Fog' in weather:
        return "Ice"
    elif 'Freezing Rain,Fog' in weather:
        return "Ice,Cloudy"
    elif 'Heavy Rain' in weather:
        return "Rain"
    elif 'Heavy Rain Showers,Moderate Snow Pellets,Fog' in weather:
        return "Rain,Snow,Cloudy"
    elif 'Heavy Rain,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Heavy Rain, Moderate Hail,Fog' in weather:
        return "Rain,Ice,Cloudy"
    elif 'Ice Pellets' in weather:
        return "Ice"
    elif 'Mainly Clear' in weather:
        return "Clear"
    elif 'Moderate Rain' in weather:
        return "Rain"
    elif 'Moderate Rain,Drizzle' in weather:
        return "Rain"
    elif 'Moderate Rain Showers' in weather:
        return "Rain"
    elif 'Moderate Rain Showers,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Moderate Rain,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Moderate Snow' in weather:
        return "Snow"
    elif 'Moderate Snow,Fog' in weather:
        return "Snow,Cloudy"
    elif 'Mostly Cloudy' in weather:
        return "Cloudy"
    elif 'Rain' in weather:
        return "Rain"
    elif 'Rain Showers' in weather:
        return "Rain"
    elif 'Rain Showers,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Rain Showers,Snow Pellets' in weather:
        return "Rain,Snow"
    elif 'Rain Showers,Snow Showers' in weather:
        return "Rain,Snow"
    elif 'Rain Showers,Snow Showers,Fog' in weather:
        return "Rain,Snow,Cloudy"
    elif 'Rain,Drizzle' in weather:
        return "Rain"
    elif 'Rain,Drizzle,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Rain,Fog' in weather:
        return "Rain,Cloudy"
    elif 'Rain,Ice Pellets' in weather:
        return "Rain,Ice"
    elif 'Rain,Snow' in weather:
        return "Rain,Snow"
    elif 'Rain,Snow,Fog' in weather:
        return "Rain,Snow,Cloudy"
    elif 'Snow' in weather:
        return "Snow"
    elif 'Snow Showers' in weather:
        return "Snow"
    elif 'Snow,Fog' in weather:
        return "Snow,Cloudy"
    elif 'Snow,Ice Pellets,Fog' in weather:
        return "Snow,Ice,Cloudy"
    elif 'Thunderstorms' in weather:
        return "Thunderstorms"
    elif 'Thunderstorms,Rain Showers' in weather:
        return "Thunderstorms,Rain"
    else:
        return weather
    
def save_image(filename):
    img = Image.open(filename)
    new_filename = filename[21:-6] 
    img.save(uncropped_destination_source + new_filename + ".jpg")

def getImage():
    
    image_files = [f for f in listdir(image_source) if isfile(join(image_source, f))]
    for img in image_files:
        save_image(image_source + img)

def getFilter(image):
    new_image=image+'.jpg'
    image_files = [f for f in listdir(uncropped_destination_source) if isfile(join(uncropped_destination_source, f))]
    for img in image_files:
        if img == new_image:
            stringSource=uncropped_destination_source+image+'.jpg'
            stringDest=new_destination_source+new_image
            os.rename(stringSource, new_destination_source+new_image)
            
def findFilter():
    weatherAttributes.apply(lambda row: getFilter(row['new_date']), axis=1)
    
            
def image_string(date):
    """ Read the date and format it to match the image file names """
    date = str(date)
    date = date.replace("-", "").replace(" ", "").replace(":", "")
    return date 

def convertWeatherDateToString():
    weatherAttributes['date']  = weatherAttributes.apply(lambda row: image_string(row['date']), axis=1)
    weatherAttributes['new_date']=weatherAttributes.apply(lambda row: image_string(row['date']), axis=1)
    
def pixelString():
    #Doing, so the string is in right format for comparision
    pixel['date'] = pixel.date.apply(lambda x: x[:-4])

def getPixels():
    #adapted from https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-using-python
    if(isfile("new_images/20171028110000.jpg")):
        os.remove(cropped_destination_source+"71028110000.jpg")
    path = r'new_images/'
    global pixel
    global samples
    global y
    global df

    count=0
    for file in os.listdir(path):
        samples=[]
        y=[]
        if file.endswith(".jpg"):
            image_name=(os.path.join(file))
            image_data = scipy.misc.imread(new_destination_source+ image_name)
            #,flatten=True, mode='RGB')
            samples.append(image_data)
            y.append(image_name) 
            
            if (count==0):
                pixel=pd.DataFrame.from_records(samples)
                df = pd.DataFrame({'date' : y})  
            elif(count>0):
                pixel2=pd.DataFrame.from_records(samples)
                pixel=pixel.append(pixel2, ignore_index=True)
                
                df2 = pd.DataFrame({'date' : y})
                df=df.append(df2, ignore_index=True)
        count=count+1       
    #data of dates and pixel  
    #format string
    pixel['date'] = df
    pixelString()

    
def joinDate():
    #function to put two data frame in right format
    convertWeatherDateToString()
    global pixel_set
    pixel_set=pd.merge(pixel, weatherAttributes,how='inner',on='date')

def applyLabel():
    weatherAttributes['Weather']  = weatherAttributes.apply(lambda row: editLabel(row['Weather']), axis=1)
#     print(pixel)
    
def toCsv():
     path_ = r'csv_all_data'
     pixel_set.to_csv(os.path.join(path_, 'weather_imagetestRGB.csv'))
    
def main(): 
    #how to run this code:
    # makes sure to create empty folder of uncropped_images, new_images and csv_all_data
    
    # What does each function do?
    #getWeather() extracts the data from a CSV and we remove all the NA values and extra columns
    #applylabel() solves the multi-label problem by labeling it to clear labels
    #getImage() grabs the file name of each image and saves it
    #convert weatherdatetoString() grabs filename and renames it 
    # findfilters filters matching dates and saves it to new file
    #getPixel() grabs every pixel and saves it to array
    # does join on dates 
    
    
    getWeather()  
    print('start')
    applyLabel()
    getImage()
    convertWeatherDateToString()
    findFilter()
    print('start')
    getPixels() 
    joinDate()   
    toCsv()

    
if __name__ == "__main__":
    main()
