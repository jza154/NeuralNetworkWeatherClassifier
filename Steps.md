PART1
NOTE: you can either use PART1 and run the commands:

Download the files from 

https://drive.google.com/open?id=1NkbYLCBRNY8gR_3X6QNPOz9vNXBYYzpA

Put all the folders downloaded with data.py analysis.py feelslike.py

Make sure you have all the folder with exact name downloaded and do not change the filename

Commands:

This is for weather label:

python data.py
python analysis.py


This is for feels like temperature:

python feelslike.py


OR go to PART2 and delete every file in the repository except for:

data.py
analysis.py
feelslike.py

and follow the instructions listed below
for more information visit PART2



----------------------------------------------------------------
PART2

required libraries:
glob
pandas
numpy
matplotlib
skimage
sklearn
os
scipy
re
glob
PIL
sys
pykalman



files expected:

CREATE folder 	csv_all_data 		and DO NOT add anything

CREATE folder 	katkam-scaled 		and ADD about 500 random katkam webcam images from the original set of images

CREATE folder	new_images		and DO NOT add anything

CREATE folder	uncropped_images	and DO NOT add anything

CREATE folder	weather			and ADD all the csv files from weather.zip

CREATE folder	weather_train_set	and ADD all the csv files from weather.zip

CREATE folder	weather_test_set	and ADD all the csv files from weather.zip



files produced:

folders new_images, uncropped_images are filled up with images

folder csv_all_data has 1 csv file added to it

file smoothed.png in the main folder


commands and arguments in order:

Using a WINDOWS machine:

put the files:

data.py

analysis.py

feelslike.py

in the same folder as the 7 folders that you created.

then open an ANACONDA command prompt in that same main folder.

then run these commands in order:

python data.py

python analysis.py

python feelslike.py




Note: running analysis.py gives you an accuracy score in the end
and running feelslike.py gives a diagram with the feels like temperature

