
# 🌇 MDA Exam Project
This project is done for the assignment project of Modern Data Analytics in academic year 2022-2023.<br />
The goal of the project is predicting crowds by estimate the noisiness at several places along Naamsestraat in Leuven.

## Contents
- [01_Data_collection](https://github.com/SarahSchrevens/MDA_project/tree/main/01_Data_collection)
- [02_Weather_data_preprocessing](https://github.com/SarahSchrevens/MDA_project/tree/main/02_Weather_data_preprocessing) 
- [03_Noise_modelling](https://github.com/SarahSchrevens/MDA_project/tree/main/03_Noise_modelling) 
- [04_App](https://github.com/SarahSchrevens/MDA_project/tree/main/04_App) 

## 1️⃣ Data_collection
The provided noise data set was collected at the 9 locations in the neighbourhood of Naamsestraat in the city of Leuven in 2022.<br />
To predict noisiness, we collected several types of datasets in addition to the provided meteo data.<br />
The codes for scraping these datasets are available in this folder.<br />
### Event Data
Assuming the crowdedness is influenced by the events in Leuven, we gather event data from the following webpages:
- [Het Depot](https://www.hetdepot.be/programma?page1)
- [LOKO](https://www.loko.be/en/past-events)
- [Belgian schools](https://schoolvakanties-be.be/schoolvakanties-2022/)
### Weather Data
To get more weather data, the following source was used:
- [wunderground](https://www.wunderground.com/weather/be/leuven/50.88,4.70)
## 2️⃣ Weather_Data_preprocessing
The used meteo data source is [here](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/SSRN3F)
To obtain past weather data, a selection of 7 weather stations near Naamsestraat (LC:065,087,102,109,112,117,118) was made.
These stations were used to create an averaged weather dataset.

## 3️⃣ Noise_modelling
We predict the hourly crowd levels by determining whether the location is noisier than usual.<br />
We created baseline thresholds for classification and developed an hourly binary classification model.<br />
This folder comprises a code for making an hourly-based feature matrix and variables, conducting EDA for feature selection, and evaluating models.<br />
The best performing model in our results was RandomForest, achieving an accuracy of approximately 80%.

## 4️⃣ App
This folder contains the scripts used for applications.<br />
We made two applications, which show real-time data and past related data.<br />
The frameworks of both apps are Plotly Dash.
### Real-time app
- This app displays real-time weather and event data, and predicts the crowdedness in places near Naamsestraat.
- The real-time weather data is collected by Weather Forecast API [Open-Meteo](https://open-meteo.com/), which allows us to gather current hourly weather data with high resolution. 
- The events data were collected by scraping the websites mentioned in the 1️⃣ Data_collection.
- For applying the model, gz.files, which are uploaded in AWS, are loaded to get the predicted values.
- [Heroku](https://www.heroku.com/) is used for web deployment.
- All the files necessary for deployment are saved in [this repository](https://github.com/Shinichi99/leuven-realtime-heroku-app)
- The app URL is https://leuven-realtime-noise.herokuapp.com/
### Past app
- This app shows the past noise, weather and event data in Leuven. 
- For studying different tools, [Render](https://render.com/) is used for web deployment.
- All the files necessary for deployment are saved in [this repository](https://github.com/Shinichi99/leuven-past-render-app)
- The app URL is https://leuven-past-noise.onrender.com/

In addition, we used Amazon S3 for data storage. The files uploaded to a S3 bucket is stored in [this folder](https://github.com/SarahSchrevens/MDA_project/tree/main/04_App/AWS)

## Appendix
In this project, we utilized Python 3.9.5, which was used in the lecture, to set up a virtual environment.<br />
The necessary packages are listed in the requirements.txt file.
