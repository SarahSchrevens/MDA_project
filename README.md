
# 🌇 MDA Exam Project
This project is done for the assignment project of Modern Data Analytics in academic year 2022-2023.
The goal of the project is predicting crowds by estimate the noisiness at several places along the  Naamse straat in Leuven.

## Table of Contents
- [01_Data_collection](https://github.com/SarahSchrevens/MDA_project/tree/main/01_Data_collection)
- [02_Weather_data_preprocessing](https://github.com/SarahSchrevens/MDA_project/tree/main/02_Weather_data_preprocessing) 
- [03_Noise_modelling](https://github.com/SarahSchrevens/MDA_project/tree/main/03_Noise_modelling) 
- [04_App](https://github.com/SarahSchrevens/MDA_project/tree/main/04_App) 

## 1️⃣ Data_collection
In order to predict crowds, we use several types of dataset.
### Meteo Data
The used meteo data source is [here](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/SSRN3F)
### Noise Data
The provided noise data set was collected at the 9 locations in neighbourhood of the Naamse straat in the city of Leuven in 2022.
### Event Data
Assuming the crowdness is correlated to the events in Leuven, we gather the following data.
- Het Depot(https://www.hetdepot.be/programma?page1)
- LOKO (https://www.loko.be/en/past-events)
- Belgian schools (https://schoolvakanties-be.be/schoolvakanties-2022/)

## 2️⃣ Weather_Data_preprocessing
This folder has Jupyter Notebooks on the preprocessing steps used for the weather data given for the project.

## 3️⃣ Noise_modelling
This folder comprises of the model training itself in regards to the noise data being predicted by several variables.

## 4️⃣ App
This folder contains the scripts used for applications.
We made two applications, which show real-time data and past related data.
The frameworks of both apps are Plotly Dash.
###　Real-time app
This app displays real-time weather and event data, and predicts the crowdedness in places near Naamse straat.
The real-time weather data is collected by Weather Forecast API [Open-Meteo](https://open-meteo.com/), which allows us to gather current hourly weather data with high resolution. The events data were collected by scraping the websites mentioned in the 1️⃣ Data_collection.
For applying the model, gz.files, which are uploaded in AWS, are loaded to get the predicted values.
[Heroku](https://www.heroku.com/) is used for web deployment.
All the files necessary for deployment are saved in [this repository](https://github.com/Shinichi99/leuven-realtime-heroku-app)
The app URL is https://leuven-realtime-noise.herokuapp.com/
###　Past app
This app shows the past noise, weather and event data in Leuven. 
For studying different tools, [Render](https://render.com/) is used for web deployment.
All the files necessary for deployment are saved in [this repository](https://github.com/Shinichi99/leuven-past-render-app)
The app URL is https://leuven-past-noise.onrender.com/

In addition, we used Amazon S3 for data storage. The files uploaded to a S3 bucket is stored in [this folder](https://github.com/SarahSchrevens/MDA_project/tree/main/04_App/AWS)

## Appendix
Beyond installing packages in requirements.txt
