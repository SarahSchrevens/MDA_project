
# 🌇 MDA Exam Project - Team Haiti
This is the final project of Team Haiti for Modern Data Analytics in the academic year 2022-2023.<br />
The objective of the project is to predict crowd density by estimating the noise levels at multiple locations along Naamsestraat in Leuven.

## Content
- [01_Data_collection](https://github.com/SarahSchrevens/MDA_project/tree/main/01_Data_collection)
- [02_Weather_data_preprocessing](https://github.com/SarahSchrevens/MDA_project/tree/main/02_Weather_data_preprocessing) 
- [03_Noise_modelling](https://github.com/SarahSchrevens/MDA_project/tree/main/03_Noise_modelling) 
- [04_App](https://github.com/SarahSchrevens/MDA_project/tree/main/04_App) 

## 1️⃣ Data collection
The provided noise dataset was collected for each of the 9 locations in the Naamsestraat in 2022.<br />
To predict noisiness, we retrieved further data in addition to the provided meteo data.<br />
The code to scrape these datasets are available in the following folders:<br />
### Event Data
Assuming the crowdedness is influenced by the events in Leuven, we gather data on events and holidays from the following webpages:
- [Het Depot](https://www.hetdepot.be/programma?page1)
- [LOKO](https://www.loko.be/en/past-events)
- [Belgian schools](https://schoolvakanties-be.be/schoolvakanties-2022/)
### Weather Data
To get more weather data, the [Open-Meteo](https://open-meteo.com/) source was used.

## 2️⃣ Weather Data Preprocessing
The used meteo data source is [here](https://rdr.kuleuven.be/dataset.xhtml?persistentId=doi:10.48804/SSRN3F)<br />
To obtain past weather data, a selection of 7 weather stations near Naamsestraat (LC:065,087,102,109,112,117,118) was made.<br />
These stations were used to create an averaged weather dataset.

## 3️⃣ Noise Modeling
We then predicted the hourly crowd levels by determining whether the location was noisier than usual.<br />
We created baseline thresholds for classification and developed an hourly binary classification model.<br />
This folder comprises the code employed to make an hourly-based feature matrix and the variables, by conducting EDA for feature selection and evaluation of the models.<br />
The best performing model was RandomForest, through with we achieved an accuracy of approximately 80%.

## 4️⃣ The app
This folder contains instead the scripts used for the applications.<br />
We made two applications, which show respectively real-time data and past related data.<br />
The framework used for both apps was Plotly Dash.
### Past app
- This app shows the past noise, weather and event data in Leuven. 
- For studying different tools, [Render](https://render.com/) is used for web deployment.
- All the files necessary for the deployment are saved in [this repository](https://github.com/Shinichi99/leuven-past-render-app)
- The final app URL is https://leuven-past-noise.onrender.com/
### Real-time app
- This app displays real-time weather and event data, and predicts the crowdedness in the selected spots near Naamsestraat.
- The real-time weather data is collected by Weather Forecast API [Open-Meteo](https://open-meteo.com/), which allows us to gather current hourly weather data with high resolution. 
- The events data were collected by scraping the websites mentioned in the 1️⃣ Data_collection.
- For applying the model, gz.files, which are uploaded in AWS, are loaded to get the predicted values.
- [Heroku](https://www.heroku.com/) is used for web deployment.
- All the files necessary for the deployment are saved in [this repository](https://github.com/Shinichi99/leuven-realtime-heroku-app)
- The finall app URL is https://leuven-realtime-noise.herokuapp.com/

In addition, we used Amazon S3 for data storage. The files uploaded to a S3 bucket is stored in [this folder](https://github.com/SarahSchrevens/MDA_project/tree/main/04_App/AWS)

## Appendix
In this project, we utilized Python 3.9.5, which was used in the lecture, to set up a virtual environment.<br />
The necessary packages are listed in the requirements.txt file.
