import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import date, timedelta
import requests #library needed for requesting permission to website
from bs4 import BeautifulSoup #needed for filtering through website html code
import re
import selenium
from selenium import webdriver
from functools import reduce
import time
import datetime
import gzip
import joblib

#Function for data scraping
def scrape_loko_data():
    ##adding url of site needed for data
    url = "https://www.loko.be/en/past-events"
    response = requests.get(url)
    ##storing in beautifulsoup element for further usage
    soup = BeautifulSoup(response.text, "html.parser")
    ##select the class from the html code we are interested in, all events we need are of this type
    dates = soup.select('div[class="card__img card__img-blue"]') 
    ##print only the text that is stored in the results element, which are only dates in this case
    date = []
    for x in dates:
        date.append(x.text)
    ##making the scraped items str format and checking the string
    date = str(date)
    ##replacing the parts that can not be included in the dataframe with blanks + checking again
    date = date.replace('\\n', '')
    ##creating a dataframe from the scraped dates 
    date = eval(date)
    df_date = pd.DataFrame(date)
    ##scraping the event titles
    titles = soup.select('h3[class="heading--4 card__title"]') 
    ##storing the events titles in a list
    title = []
    for y in titles:
        title.append(y.text)
    ##converting the event titles in the title list into a string format
    title = str(title)
    ##replace the parts that are not needed in the dataframe by blanks
    title = title.replace('\\n', "")
    ##creating a datframe from the scraped event titles
    title = eval(title)
    df_title = pd.DataFrame(title)
    ##making one joined df from the date and event df's + checking the new df
    frames = [df_date, df_title]
    df = pd.concat(frames, axis = 1, join = 'inner')
    df.columns=['dates','event']
    df_event = date_split(df)
    return df_event

def scrape_school_data():
    ##adding url of site needed for data
    url = "https://schoolvakanties-be.be/schoolvakanties-2023/"
    response = requests.get(url)
    ##storing in beautifulsoup element for further usage
    soup = BeautifulSoup(response.text, "html.parser")
    ## scraping the Belgian school holidays
    holidays = soup.select('span[class="event-place"]') 
    ## store the holidays in a list
    holiday = []
    for y in holidays:
        holiday.append(y.text)
    ## create a dataframe from the holidays
    df_holiday = pd.DataFrame(holiday)
    ## select the startdate of the school holidays in Belgium
    starts = soup.select('span[itemprop="startDate"]') 
    ## store the start dates in a list
    start = []
    for z in starts:
        start.append(z.text)
    ##format the dates in the list in string format
    start = str(start)
    ## creating a list of weekdays in dutch for removal
    days = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']
    ## creating a regular expression for searching through the text and removing the days
    pattern = re.compile(r'\b(?:{})\b'.format('|'.join(days)), flags=re.IGNORECASE)
    ## replacing the days with a blank
    en_start = pattern.sub('', start)
    ## translating the dutch months into english months for formating datetime format
    en_start = en_start.replace("januari", "january")
    en_start = en_start.replace('februari', 'february')
    en_start = en_start.replace('maart', 'march')
    en_start = en_start.replace('mei', 'may')
    en_start = en_start.replace('juni', 'june')
    en_start = en_start.replace('juli', 'july')
    en_start = en_start.replace('augustus', 'august')
    en_start = en_start.replace('oktober', 'october')
    en_start = en_start.replace(' ', '')
    ## creating a df from the start dates of the holidays
    en_start = eval(en_start)
    df_start = pd.DataFrame(en_start)
    ## scraping the enddate of the belgian school holidays
    ends = soup.select('span[itemprop="endDate"]') 
    ## storing the scraping results in a list
    end = []
    for i in ends:
        end.append(i.text)
    ## format the list into string format
    end = str(end)
    ## searching for the dutch days in the string and remove them/replace them with a blank
    en_end = pattern.sub('', end)
    ## translating the dutch names into englisch names for the months
    en_end = en_end.replace("januari", "january")
    en_end = en_end.replace('februari', 'february')
    en_end = en_end.replace('maart', 'march')
    en_end = en_end.replace('mei', 'may')
    en_end = en_end.replace('juni', 'june')
    en_end = en_end.replace('juli', 'july')
    en_end = en_end.replace('augustus', 'august')
    en_end = en_end.replace('oktober', 'october')
    en_end = en_end.replace(' ', '')
    ## creating a new df from the end dates of the belgian school holidays
    en_end = eval(en_end)
    df_end = pd.DataFrame(en_end)
    ## creating a new df from the holidays with their start- and enddate
    frames = [df_holiday, df_start, df_end]
    df = pd.concat(frames, axis = 1, join = 'inner')
    df.columns =['Holiday', 'StartDate', 'EndDate']
    return df


def scrape_depot_data():
    thislist1 = []
    thislist2 = []
    for i in range(0,2):
        s = str(i)
        url = "https://www.hetdepot.be/programma?page=" + s
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        groups = soup.select('div.calendar__group')
        for group in groups:
            date = group.select_one('h3').text.strip()
            items = group.select('div.calendar-item')
            for item in items:
                title = item.select_one('h2.calendar-item__title').text.strip()
                thislist1.append(title)
                thislist2.append(date)
    df_next = pd.DataFrame(thislist1)
    df_next.columns = ["Event Name"]
    df_next['Date'] = thislist2
    #create dataframe only date
    df_only_date = df_next.loc[:, ["Date"]]
    list1 = []
    list2 = []

    for i in range(len(df_only_date)):
        ser = df_only_date.loc[i]
        series = ser.to_string()
        all_words = str.split(series)
        if len(all_words) == 4:
            #extract second word of each row
            second_word = all_words[1]
            #split word
            last_two = second_word[-2:]
            rest = second_word[:-2]
            result = rest + " " + last_two 
            #replace
            words = result.split() #split first word
            words[0] = "" #first word replaced with empty space
            new_string = " ".join(words) #adding rest to empty space to get only number
            #get rest of the words
            month = all_words[2] #get third word
            month = str(month) 
            year = all_words[3] #get fourth word
            year = str(year)
            final = year + month + new_string #put together
            new_final = f"{year} {month} {new_string}" #format
            new_final = new_final.replace("jan", "01")
            new_final = new_final.replace('feb', '02')
            new_final = new_final.replace('mrt', '03')
            new_final = new_final.replace('apr', '04')
            new_final = new_final.replace('mei', '05')
            new_final = new_final.replace('jun', '06')
            new_final = new_final.replace('jul', '07')
            new_final = new_final.replace('aug', '08')
            new_final = new_final.replace('sep', '09')
            new_final = new_final.replace('okt', '10')
            new_final = new_final.replace('nov', '11')
            new_final = new_final.replace('dec', '12')
            new_final = new_final.replace('  ', ' ')
            new_final = new_final.replace(' ', '-')
            list1.append(new_final)
        else:
            #extract second word of each row
            second_word2 = all_words[1]
            last_two2 = second_word2[-2:]
            rest2 = second_word2[:-2]
            result2 = rest2 + " " + last_two2
            #replace
            words2 = result2.split() #split first word
            words2[0] = "" #first word replaced with empty space
            new_string2 = " ".join(words2) #adding rest to empty space to get only number
            #get month
            month2 = all_words[2] #get third word
            month2 = str(month2) 
            #extract year (fourth word)
            fourth_word = all_words[3]
            #keep only first 4 characters
            first_four = fourth_word[:4]
            str(first_four)
            final_ee = first_four + month2 + new_string2 #put together
            final_e = f"{first_four} {month2} {new_string2}" #format
            final_e = final_e.replace("jan", "01")
            final_e = final_e.replace('feb', '02')
            final_e = final_e.replace('mrt', '03')
            final_e = final_e.replace('apr', '04')
            final_e = final_e.replace('mei', '05')
            final_e = final_e.replace('jun', '06')
            final_e = final_e.replace('jul', '07')
            final_e = final_e.replace('aug', '08')
            final_e = final_e.replace('sep', '09')
            final_e = final_e.replace('okt', '10')
            final_e = final_e.replace('nov', '11')
            final_e = final_e.replace('dec', '12')
            final_e = final_e.replace('  ', ' ')
            final_e = final_e.replace(' ', '-')
            list1.append(final_e)
        if len(all_words) == 6:
            #extract fourth word of each row
            fourth_word = all_words[3]
            #keep only last 2 characters
            last_two3 = fourth_word[-2:]
            str(last_two)
            #get rest of the words
            month3 = all_words[4] #get fifth word
            month3 = str(month3) 
            year3 = all_words[5] #get sixth word
            year3 = str(year3)
            final3 = year3 + month3 + last_two3 #put together
            new_final2 = f"{year3} {month3} {last_two3}" #format
            new_final2 = new_final2.replace("jan", "01")
            new_final2 = new_final2.replace('feb', '02')
            new_final2 = new_final2.replace('mrt', '03')
            new_final2 = new_final2.replace('apr', '04')
            new_final2 = new_final2.replace('mei', '05')
            new_final2 = new_final2.replace('jun', '06')
            new_final2 = new_final2.replace('jul', '07')
            new_final2 = new_final2.replace('aug', '08')
            new_final2 = new_final2.replace('sep', '09')
            new_final2 = new_final2.replace('okt', '10')
            new_final2 = new_final2.replace('nov', '11')
            new_final2 = new_final2.replace('dec', '12')
            new_final2 = new_final2.replace('  ', ' ')
            new_final2 = new_final2.replace(' ', '-')
            list2.append(new_final2)
        else:
            list2.append(new_final)
    #create final DataFrame
    df_next = pd.DataFrame(thislist1)
    df_next.columns = ["Event Name"]
    df_next["StartDate"] = list1
    df_next["EndDate"] = list2
    
    return df_next

def scrap_weather_data():
    colnames = ['Time','Conditions','LC_TEMP_QCL3_list','Feels_Like','Precipitation_Chance',
            'LC_RAININ','Cloud_Cover','Dew_Point','LC_HUMIDITY','Wind','Pressure']
    def hour_mess(date_iter,data,colnames=colnames):
        timevals = (pd.DataFrame([data[i:i+10] for i in range(0, len(data), 11 )])
                .pipe(lambda x: x.iloc[:, 0]).rename('datetime',inplace=True).to_frame()
                .pipe(lambda x: x.assign(Time=date_iter + ' ' + x['datetime'])).drop('datetime',axis=1)
                .pipe(lambda x: x.assign(Time=pd.to_datetime(x['Time'], format='%Y-%m-%d %I:%M %p',utc=True))))
        cvals = pd.DataFrame([data[i] for i in range(1, len(data), 11)], columns=[colnames[1]])
        tempvals = (pd.DataFrame([data[i:i+10] for i in range(2, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)')).pipe(lambda x: x.astype(float))
               .pipe(lambda x: x.rename(columns={0: 'LC_TEMP_QCL3_list'})).pipe(lambda x: (x-32)*5/9))
        flvals = (pd.DataFrame([data[i:i+10] for i in range(3, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)')).pipe(lambda x: x.astype(float))
               .pipe(lambda x: x.rename(columns={0: 'Feels_Like'})).pipe(lambda x: (x-32)*5/9))
        pcvals = (pd.DataFrame([data[i:i+10] for i in range(4, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)'))
               .pipe(lambda x: x.astype(int)).pipe(lambda x: x.rename(columns={0: 'Precipitation_Chance'})))
        drsvals = (pd.DataFrame([data[i:i+10] for i in range(5, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)')).pipe(lambda x: x.astype(int))
               .pipe(lambda x: x.rename(columns={0: 'LC_RAININ'})).pipe(lambda x: x*25.4))
        ccvals = (pd.DataFrame([data[i:i+10] for i in range(6, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)'))
               .pipe(lambda x: x.astype(int)).pipe(lambda x: x.rename(columns={0: 'Cloud_Cover'})))
        dpvals = (pd.DataFrame([data[i:i+10] for i in range(7, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)'))
               .pipe(lambda x: x.astype(float)).pipe(lambda x: x.rename(columns={0: 'Dew_Point'})).pipe(lambda x: (x-32)*5/9))
        hvals = (pd.DataFrame([data[i:i+10] for i in range(8, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)'))
               .pipe(lambda x: x.astype(int)).pipe(lambda x: x.rename(columns={0: 'LC_HUMIDITY'})))
        wvals = (pd.DataFrame([data[i:i+10] for i in range(9, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)')).pipe(lambda x: x.astype(float)).pipe(lambda x: x / 2.237)
               .pipe(lambda x: x.rename(columns={0: 'Wind'})))
        pvals = (pd.DataFrame([data[i:i+9] for i in range(10, len(data), 11)])
               .pipe(lambda x: x.iloc[:, 0]).pipe(lambda x: x.str.extract('(\d+)')).pipe(lambda x: x.astype(int))
               .pipe(lambda x: x.rename(columns={0: 'Pressure'})).pipe(lambda x: x*33.8627906977))

        df_data = pd.concat(objs=[timevals,cvals,tempvals,flvals,pcvals,
                              drsvals,ccvals,dpvals,hvals,wvals,pvals],axis=1)
        return df_data

    def render_page(url):
            driver = webdriver.Chrome()
            driver.get(url)
            driver.implicitly_wait(5)
            time.sleep(5) #open content and so it fully renders, then parse it. crawl delay is 10 seconds at least, so make it 11 for ethics.
            r = driver.page_source
            driver.quit()
            return r

    dates = [datetime.datetime.now().strftime('%Y-%m-%d')] #assume only one day is needed for this one.
    page = 'https://www.wunderground.com/hourly/be/leuven/date/' #the main page for the leuven hourly forecast data.

    combined_output = pd.DataFrame()
    #colnames has been defined above in the collapsed cell block
    for date_iter in dates:
        url = str(str(page)+str(date_iter))
        r = render_page(url)
        soup = BeautifulSoup(r, "html.parser")
        container = soup.find('lib-city-hourly-forecast')
        check = container.find('tbody') #the part of the site i actually want

        data = []
        for c in check.find_all('tr', class_='mat-row cdk-row ng-star-inserted'):
            for i in c.find_all('td', class_='ng-star-inserted'):
                trial = i.text
                trial = trial.strip('  ')
                data.append(trial)
    
        output=hour_mess(date_iter=date_iter,data=data,colnames=colnames)
        combined_output = pd.concat(objs=[combined_output,output])
    return combined_output

#Function for realtime data predictors
def date_split(df):
    for i, row in df.iterrows():
        date_range = row['dates'].split('-')
        startdate = date_range[0].strip()
        if len(date_range) == 1:
            enddate = startdate
        else:
            enddate = date_range[1].strip()
        df.loc[i, 'startdate'] = startdate
        df.loc[i, 'enddate'] = enddate
    df = df.drop('dates', axis=1)
    return df

def weekend_daytime(df):
  df['Thursday-Friday'] = df['weekday'].isin(['Thursday','Friday']).astype(int)
  df['Saturday'] = df['weekday'].isin(['Saturday']).astype(int)
  df['Sunday'] = df['weekday'].isin(['Sunday']).astype(int)
  df['late-at-night'] = df['start_hour'].isin([1,2,3,4,5,6,7]).astype(int)
  df['evening'] = df['start_hour'].isin([20,21,22]).astype(int)
  df['summer'] = (df['date'] >= '2022-07-01') & (df['date'] <= '2022-08-31')
  df['summer'] = df['summer'].astype(int)
  return df

#Real time dataframe
def realtime_data(df_weather=None, event_data_school=None, event_data_loko=None, event_data_depot=None):
    location = ['Number 35' ,'Number 57' ,'Number 62',
 'Number 76 ("His & Hears” Hair salon in Leuven)',
 'Calvarie Chapel (near the Faculty of Economics)',
 'Corner of the Parkstraat & Naamse straat', 'Number 81' ,
 'Vrijthof']
    Latitude = [50.87714563, 50.87650836, 50.87585017, 50.875262,   50.87452363, 50.87423614,
 50.87382304, 50.87874797]
    Longitude = [4.70068783, 4.700571,   4.70020261, 4.70010208, 4.69990663, 4.70003239,
 4.70004193, 4.70113378]
    columns = ['location', 'Latitude', 'Longitude', 'date', 'start_hour', 'weekday',
               'LC_HUMIDITY', 'LC_RAININ', 'LC_TEMP_QCL3_list', 'school', 'loko', 'depot']
    
    if df_weather is None:
        # Return an empty DataFrame with the required columns
        empty_df = pd.DataFrame(columns=columns)
        return empty_df

    df = pd.DataFrame({'location': location, 'Latitude': Latitude, 'Longitude': Longitude})

    df['date'] = datetime.datetime.now().date()
    # Convert the 'date' column to datetime.date type
    df['date'] = pd.to_datetime(df['date'])
    df['start_hour'] = datetime.datetime.now().hour
    df['weekday'] = datetime.datetime.now().strftime('%A')
    df['LC_HUMIDITY'] = df_weather['LC_HUMIDITY']
    df['LC_RAININ'] = df_weather['LC_RAININ']
    df['LC_TEMP_QCL3_list'] = df_weather['LC_RAININ']
    df['school'] = len(event_data_school)
    df['loko'] = len(event_data_loko)
    df['depot'] = len(event_data_depot)
    df=weekend_daytime(df)
    
    #model fitting
    # Define the base URL and output file names
    base_url = 'https://mda-noise.s3.eu-central-1.amazonaws.com/model_df_'
    output_files = ['df_01_model.gz', 'df_02_model.gz', 'df_03_model.gz', 'df_04_model.gz', 'df_05_model.gz', 'df_06_model.gz', 'df_07_model.gz', 'df_08_model.gz']

    # Create a new column 'Y' in the DataFrame
    df['Y'] = None

    #predictor variables
    predictor_vars = ['LC_HUMIDITY', 'LC_RAININ', 'LC_TEMP_QCL3_list', 'school', 'loko', 'depot', 'Thursday-Friday', 'Saturday', 'Sunday', 'late-at-night', 'evening', 'summer']

    # Iterate over the rows of the DataFrame
    for i, row in df.iterrows():
        # Get the model index corresponding to the row index (assuming row index starts from 0)
        model_index = i
    
        # Construct the URL for the current model
        url = base_url + f'{model_index+1:02}.gz'
    
        # Specify the output file name
        output_file = output_files[model_index]
    
        # Download the .gz file
        response = requests.get(url)
    
        # Extract the contents of the .gz file
        extracted_data = gzip.decompress(response.content)
    
        # Save the extracted model to a file
        with open(output_file, 'wb') as output:
            output.write(extracted_data)
    
        # Load the extracted model
        with open(output_file, 'rb') as file:
            model = joblib.load(file)
    
    
        # Get the predictor variables for the current row
        X = row[predictor_vars].values.reshape(1, -1)
        
        # Assign the column names to X
        X = pd.DataFrame(X, columns=predictor_vars)
        
        # Fit the model to the predictor variables
        y_pred = model.predict(X)
    
        # Update the 'Y' column with the predicted value
        df.at[i, 'Y'] = y_pred[0]

    # Map the values in the 'Y' column
    df['Y'] = df['Y'].map({False: 'Normal', True: 'Busier than usual'})
    return df

# Define the function to plot the map
def plot_map(df_weather=None, event_data_school=None, event_data_loko=None, event_data_depot=None):
    
    # Set the mapbox access token
    mapbox_access_token = 'pk.eyJ1IjoiY2hpYW0wMzgiLCJhIjoiY2xnemFpODRrMGhqOTNwb2d6ZHF4MGN4aiJ9.TNlviVcT53vGInxiKM-vxQ'
    
    selected_data=realtime_data(df_weather,event_data_school,event_data_loko,event_data_depot)
    # Define the layout of the map using Mapbox
    layout = go.Layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='mapbox://styles/mapbox/light-v10', # Set the style 
            center=dict(lon=4.700700, lat=50.876490), # Set the center of the map to Naamsestraat
            zoom=15, # Set the zoom level
            ),
        )
    
    trace = None
    # Check if there is any data in the filtered_data dataframe
    if not selected_data.empty:
        # Define the data for the map
        lon = selected_data['Longitude'] 
        lat = selected_data['Latitude'] 
        predict = selected_data['Y']
        name = selected_data['location']
    
        # Define the data for the map
        trace = go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=dict(
                size=10,
                sizemode='diameter',
                color=predict.map({'Normal': 'blue', 'Busier than usual': 'red'}),  # Map 'Normal' to blue and 'Busier than usual' to red
            ),
            hovertemplate='<b>%{text}</b><br>Predicted situation: %{customdata}<extra></extra>',
            text=name,
            customdata=[[situation] for situation in predict]
        )
    
            # Create the map with go.Scattermapbox
    fig = go.Figure(data=trace, layout=layout)
    fig.update_layout(layout,height=600)
        
    # Show the map
    return fig

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# define backgorund of app 
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


# Define the layout of the app
app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([
                dcc.Markdown('Noise Level in Naamsestraat - Leuven',style={ 'textAlign':'center', 'font-weight': 'bold', 'font-size': '35px', 'font-style': 'italic', 'text-decoration': 'underline'})
        ],width=12)
    ]),

    dbc.Row([dcc.Markdown('**Real time data extraction** \U0001F4C5',
                         style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
             html.Button('Click here to see the content', id='btn-nclicks-1'),        
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Graph(
                id='map-graph',
                figure=plot_map(df_weather=None, event_data_school=None, event_data_loko=None, event_data_depot=None)
            )],width=8), 

         dbc.Col([
             dbc.Row([
                dcc.Markdown('**Weather**' + "\u2600"),
                html.Div([
                html.Span("Humidity: ", style={"font-weight": "bold"}),
                html.Span(id='humidity'),
            ]),
                html.Div([
                html.Span("Rain: ", style={"font-weight": "bold"}),
                html.Span(id='rainin'),
            ]),
                html.Div([
                html.Span("Temperature: ", style={"font-weight": "bold"}),
                html.Span(id='temp_qcl3'),
            ])               
                ]),
            
    html.Hr(),  # Add a horizontal line 

            dbc.Row([
            dcc.Markdown('**Depot events**' + "\U0001F389"),
            html.Div(id='event_title')            
        ]),

    html.Hr(),  # Add a horizontal line 

            dbc.Row([
            dcc.Markdown('**Loko events**' + "\U0001F389"),
            html.Div(id='event_title2')            
        ]),

    html.Hr(),  # Add a horizontal line 

            dbc.Row([
            dcc.Markdown('**School holidays**' + "\U0001F3EB"),
            html.Div(id='event_title3')            
        ]),

        ], style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
    ])
], style={'background-color': '#ADD8E6'})

# Define the callback function to update the map based on the selected date and time
@app.callback(Output('map-graph', 'figure'),
              Output('event_title', 'children'),
              Output('event_title2', 'children'),
              Output('event_title3', 'children'),
              Output('humidity', 'children'),
              Output('rainin', 'children'),
              Output('temp_qcl3', 'children'),              
              Input('btn-nclicks-1', 'n_clicks'))

# function to update information based on date and time
def update_data(n_clicks):

    current_date = datetime.datetime.now().date()

    #depot update
    event_data_depot = scrape_depot_data()
    event_data_depot['StartDate'] = pd.to_datetime(event_data_depot['StartDate']).dt.date  
    event_data_depot['EndDate'] = pd.to_datetime(event_data_depot['EndDate']).dt.date
    event_data_depot = event_data_depot[(event_data_depot["StartDate"] <= current_date) & (event_data_depot["EndDate"] >= current_date)]
    event_title = event_data_depot['Event Name'].tolist()

    #loko update
    event_data_loko = scrape_loko_data()
    event_data_loko["startdate"] = pd.to_datetime(event_data_loko["startdate"], format="%d %b %Y").dt.date
    event_data_loko["enddate"] = pd.to_datetime(event_data_loko["enddate"], format="%d %b %Y").dt.date
    event_data_loko = event_data_loko[(event_data_loko["startdate"] <= current_date) & (event_data_loko["enddate"] >= current_date)]
    event_title2 = event_data_loko['event'].tolist()

    #school update
    event_data_school = scrape_school_data()
    event_data_school["StartDate"] = pd.to_datetime(event_data_school["StartDate"], format="%d%B%Y").dt.date
    event_data_school["EndDate"] = pd.to_datetime(event_data_school["EndDate"], format="%d%B%Y").dt.date
    event_data_school = event_data_school[(event_data_school["StartDate"] <= current_date) & (event_data_school["StartDate"] >= current_date)]
    event_title3 = event_data_school['Holiday'].tolist()

    #weather update
    df_weather = scrap_weather_data()
    df_weather = df_weather.iloc[0]
    humidity = df_weather['LC_HUMIDITY'].tolist()
    rainin = df_weather['LC_RAININ'].tolist()
    temp_qcl3 = df_weather['LC_TEMP_QCL3_list'].tolist()
    
    fig = plot_map(df_weather, event_data_school, event_data_loko, event_data_depot)
        
    #conditions for update to happen

    if len(event_title) > 0:
        event_title = "   ;   ".join(event_title)  # separate by ; if multiple events on same day
    else:
        event_title = "No events on selected date"

    if len(event_title2) > 0:
        event_title2 = "   ;   ".join(event_title2)  # separate by ; if multiple events on same day
    else:
        event_title2 = "No events on selected date"

    if len(event_title3) > 0:
        event_title3 = "   ;   ".join(event_title3)  # separate by ; if multiple holidays on same day
    else:
        event_title3 = "No holidays on selected date"

    return fig, event_title, event_title2, event_title3, humidity, rainin, temp_qcl3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)