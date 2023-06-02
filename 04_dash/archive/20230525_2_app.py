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

# Define the function to plot the map
def plot_map(date, hour):
    # Load the dataset with noise data
    data = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/mergeddf01_df09.csv')

    # Transform first
    data['day'] = pd.to_datetime(data['day'])  # Convert the filter date to datetime type

    # Filter by date and time
    selected_data = data[(data['day'] == date) & (data['start_hour'] == hour)]
    
    # Set the mapbox access token
    mapbox_access_token = 'pk.eyJ1IjoiY2hpYW0wMzgiLCJhIjoiY2xnemFpODRrMGhqOTNwb2d6ZHF4MGN4aiJ9.TNlviVcT53vGInxiKM-vxQ'

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
        noise = selected_data['laf50_per_hour'].fillna(0) # Replace missing values with 0
        name = selected_data['location']
        
        # Calculate the sizeref value based on non-zero values of noise
        if noise.any():
            sizeref = np.array(noise[noise != 0].dropna()).max() / 20
        else:
            sizeref = 1
    
        # Define the data for the map
        trace = go.Scattermapbox(
            lat=lat,
            lon=lon,
            mode='markers',
            marker=dict(
                size=noise,
                sizemode='diameter',
                sizeref=sizeref,
                color=noise, 
                colorscale='Blues',  # Choose a colorscale
                colorbar=dict(
                    titleside='top',
                    tickmode='auto',
                    ticks='outside',
                    ticklen=5,
                    ticksuffix=' dBA',
                ),
            ),
        hovertemplate='<b>%{text}</b><br>Noise: %{marker.size} dBA<extra></extra>',
        text=name
        )
    
            # Create the map with go.Scattermapbox
    fig = go.Figure(data=trace, layout=layout)
    fig.update_layout(layout,height=600)
        
    # Show the map
    return fig

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
    df_event["startdate"] = pd.to_datetime(df_event["startdate"], format="%d %b %Y")
    df_event["enddate"] = pd.to_datetime(df_event["enddate"], format="%d %b %Y")
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
    ## formatting the dates in the datetime format + checking df
    df["StartDate"] = pd.to_datetime(df["StartDate"], format="%d%B%Y")
    df["EndDate"] = pd.to_datetime(df["EndDate"], format="%d%B%Y")
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




app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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

    dbc.Row([
        dbc.Col([
            dcc.Markdown('**Date** \U0001F4C5',
                         style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
            dcc.DatePickerSingle(
                id='date-picker',
                min_date_allowed=date(2022, 3, 1),
                max_date_allowed=date(2023, 12, 31),
                date=date(2022, 3, 1), #start from march
                display_format='DD/MM/YYYY',
                style={'margin-bottom': '20px'}
            ),
            
            dcc.Markdown('**Hour** \U0001F552',
                         style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
            dcc.Slider(
                id='hour-slider',
                min=0,
                max=23,
                value=0,
                marks={str(hour): {'label': f"{hour:02d}:00"} for hour in range(0,24)},
                step=None,
                updatemode='drag',
                included=False
            )
        ], width=8)
    ]),

    dbc.Row([

        dbc.Col([
            dcc.Graph(
                id='map-graph',
                figure=plot_map(pd.to_datetime('2022-02-03'), 10)
            )],width=8), 

         dbc.Col([
             dbc.Row([
                dcc.Markdown('**Weather**' + "\u2600"),
                html.Div(id='humidity'),
                html.Div(id='rainin'),
                html.Div(id='temp_qcl3')                
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
              Input('date-picker', 'date'),
              Input('hour-slider', 'value'))


def update_map_and_event_and_weather(date, hour):

    selected_datetime = pd.to_datetime(date)
    today = pd.Timestamp.today().date()

    if selected_datetime.date() <= today:
        event_data_depot = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/depot.csv')
        event_data_loko = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/events_loko.csv')
        event_data_school = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/school_holidays_belg.csv', encoding="mac_roman")
    else:
        event_data_depot = scrape_depot_data()
        event_data_loko = scrape_loko_data()
        event_data_school = scrape_school_data()

    #depot
    
    event_data_depot['StartDate'] = pd.to_datetime(event_data_depot['StartDate'])  # Convert StartDate to datetime type
    event_data_depot['EndDate'] = pd.to_datetime(event_data_depot['EndDate'])  # Convert EndDate to datetime type
    event_title = event_data_depot[
        (event_data_depot['StartDate'].dt.date <= selected_datetime.date()) &
        (event_data_depot['EndDate'].dt.date >= selected_datetime.date())
    ]['Event Name'].tolist()

    #loko
    
    event_data_loko['startdate'] = pd.to_datetime(event_data_loko['startdate'])  # Convert StartDate to datetime type
    event_data_loko['enddate'] = pd.to_datetime(event_data_loko['enddate'])  # Convert EndDate to datetime type
    event_title2 = event_data_loko[
        (event_data_loko['startdate'].dt.date <= selected_datetime.date()) &
        (event_data_loko['enddate'].dt.date >= selected_datetime.date())
    ]['event'].tolist()

    #school
    
    event_data_school['StartDate'] = pd.to_datetime(event_data_school['StartDate'])  # Convert StartDate to datetime type
    event_data_school['EndDate'] = pd.to_datetime(event_data_school['EndDate'])  # Convert EndDate to datetime type
    event_title3 = event_data_school[
        (event_data_school['StartDate'].dt.date <= selected_datetime.date()) &
        (event_data_school['EndDate'].dt.date >= selected_datetime.date())
    ]['Holiday'].tolist()

    #weather
    data = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/mergeddf01_df09.csv')
    data['day'] = pd.to_datetime(data['day'])
    selected_data = data[(data['day'] == date) & (data['start_hour'] == hour)]
    humidity = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_HUMIDITY'].tolist()
    rainin = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_RAININ'].tolist()
    temp_qcl3 = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_TEMP_QCL3_list'].tolist()
    
    fig = plot_map(date, hour)
        
    if len(humidity) > 0:
        humidity = humidity[0]  # Only getting the first event for now
    else:
        humidity = "No data on selected date/time"
    if len(rainin) > 0:
        rainin = rainin[0]  # Only getting the first event for now
    else:
        rainin = "No data on selected date/time"
    if len(temp_qcl3) > 0:
        temp_qcl3 = temp_qcl3[0]  # Only getting the first event for now
    else:
        temp_qcl3 = "No data on selected date/time"

    if len(event_title) > 0:
        event_title = event_title[0]  # Only getting the first event for now
    else:
        event_title = "No events on selected date"

    if len(event_title2) > 0:
        event_title2 = event_title2[0]  # Only getting the first event for now
    else:
        event_title2 = "No events on selected date"

    if len(event_title3) > 0:
        event_title3 = event_title3[0]  # Only getting the first event for now
    else:
        event_title3 = "No holidays on selected date"

    return fig, event_title, event_title2, event_title3, humidity, rainin, temp_qcl3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)