import plotly.graph_objects as go #creating interactive plots
import pandas as pd #data analysis and manipulation
import numpy as np #multi-dimensional arrays and mathematical functions
from dash import Dash, html, dcc #modules within dash that provide HTML and Dash core components
                                #respectively, for creating the user interface of the web application
import dash_bootstrap_components as dbc #dash extension that provides additional components styled using Bootstrap (CSS framework)
from dash.dependencies import Input, Output #classes to define input and output relationships between components in a Dash app
from datetime import date, timedelta #classes to work with dates and time durations in Python

#----------------------------------------------------------------------------------------------------------

# Define the function to plot the map
def plot_map(date, hour):

    # Load the dataset with noise data
    data = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/mergeddf01_df09.csv')

    # convert the 'day' column in the DataFrame data to a datetime data type. 
    # This is done to enable filtering and manipulation of dates later on
    data['day'] = pd.to_datetime(data['day'])

    # Filter by date and time
    # selects the rows where the 'day' column matches the date and the 'start_hour' column matches the hour. 
    # The filtered data is stored in the selected_data variable.
    selected_data = data[(data['day'] == date) & (data['start_hour'] == hour)]
    
    # Set the mapbox access token required to access Mapbox services
    # The access token is a string that uniquely identifies the user and authorizes access to Mapbox resources
    mapbox_access_token = 'pk.eyJ1IjoiY2hpYW0wMzgiLCJhIjoiY2xnemFpODRrMGhqOTNwb2d6ZHF4MGN4aiJ9.TNlviVcT53vGInxiKM-vxQ'

    # Define the layout of the map using Mapbox
    layout = go.Layout( # go.Layout object that specifies the settings for the map visualization
        mapbox=dict( # new dictionary object
            accesstoken=mapbox_access_token, #set the Mapbox access token
            style='mapbox://styles/mapbox/light-v10', # Set the style 
            center=dict(lon=4.700700, lat=50.876490), # Set the center of the map to Naamsestraat
            zoom=15, # Set the zoom level
            ),
        )
    
    # initialize the trace variable to None to use later to store a go.Scattermapbox object (data trace for the map visualization)
    trace = None

    # Check if there is any data in the filtered_data dataframe - if so execute if
    if not selected_data.empty:
        # Define the data for the map
        # extract specific columns from the selected_data DataFrame and assign them to individual variables
        lon = selected_data['Longitude'] 
        lat = selected_data['Latitude'] 
        noise = selected_data['laf50_per_hour'].fillna(0) # Replace missing values with 0
        name = selected_data['location']
        
        # conditional statement calculates the sizeref value based on the non-zero values of the noise array. 
        # If there are non-zero values, the max non-zero value is divided by 20 to determine the sizeref. 
        # Otherwise, if all values are zero, sizeref is set to 1.
        if noise.any():
            sizeref = np.array(noise[noise != 0].dropna()).max() / 20
        else:
            sizeref = 1
    
        # Define the data for the map - trace as a go.Scattermapbox object
        trace = go.Scattermapbox(
            # specifies the latitude and longitude coordinates
            lat=lat,
            lon=lon,
            # define the marker properties, such as size, color, and color scale
            mode='markers',
            marker=dict(
                size=noise, #size of marker depends on how noisy
                sizemode='diameter', # size represents the diameter of the markers
                sizeref=sizeref, #scaling factor ensures that size of the markers adequately represents the range of noise values
                color=noise, # Each marker will be assigned a color based on its corresponding noise value
                colorscale='Blues',  # colorscale - range of blue colors
                colorbar=dict(
                    titleside='top', #colorbar title on top
                    tickmode='auto', #automatically determine the appropriate tick marks based on the data
                    ticks='outside', #tick marks appear on the outside of the colorbar
                    ticklen=5, #length of the tick marks 5 pixels
                    ticksuffix=' dBA', #unit of measurement for the noise values
                ),
            ),
        hovertemplate='<b>%{text}</b><br>Noise: %{marker.size} dBA<extra></extra>', #text when hovering over a marker on  map
        text=name #text labels for each marker
        )
    
    # create a go.Figure object, which combines the trace and layout defined earlier. 
    # The update_layout method is used to modify the layout object by setting the height to 600 pixels.
    fig = go.Figure(data=trace, layout=layout)
    fig.update_layout(layout,height=600)
        
    # Show the map
    return fig

#----------------------------------------------------------------------------------------------------------

#creation of a Dash application using the Dash library
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP]) #CSS stylesheets Bootstrap - imported from the dash_bootstrap_components
server = app.server #Flask server object used to handle HTTP requests and responses
# By default, Dash creates a Flask server when the app variable is defined
# Assigning app.server to the server variable allows to access and configure the Flask server if needed

#----------------------------------------------------------------------------------------------------------

# define backgorund of app 
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

#----------------------------------------------------------------------------------------------------------

# Define the layout of the app
# assign the layout of the Dash application by modifying the layout attribute of the app object
app.layout = dbc.Container([ # Bootstrap container component to structure the layout of the app. 
                             # It contains rows and columns that define the arrangement of various elements.

    dbc.Row([ #row component within the container
        dbc.Col([
                # Markdown component to render text content with Markdown formatting
                dcc.Markdown('Noise Level in Naamsestraat - Leuven', style={ 'textAlign':'center', 'font-weight': 'bold', 'font-size': '35px', 'font-style': 'italic', 'text-decoration': 'underline'})
        ],width=12)
    ]),

    dbc.Row([ #row component within the container
        dbc.Col([ #column component within a row
            dcc.Markdown('**Date** \U0001F4C5',
                         style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
            # Date Picker component to allow the selection of a single date.
            dcc.DatePickerSingle(
                id='date-picker',
                min_date_allowed=date(2022, 3, 1),
                max_date_allowed=date(2022, 12, 31),
                date=date(2022, 1, 1), #start from march
                display_format='DD/MM/YYYY',
                style={'margin-bottom': '20px'}
            ),
            
            dcc.Markdown('**Hour** \U0001F552',
                         style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
            # Slider component to enable the selection of an hour value
            dcc.Slider(
                id='hour-slider',
                min=0,
                max=23,
                value=0, #starting value
                ##dictionary with labels for each hour. Slider displaying these labels at the corresponding positions
                marks={str(hour): {'label': f"{hour:02d}:00"} for hour in range(0,24)}, 
                step=None,
                updatemode='drag',
                included=False
            )
        ], width=8)
    ]),

    dbc.Row([ #row component within the container

        dbc.Col([ #column component within a row
            dcc.Graph( # Graph component to display a Plotly graph
                id='map-graph',
                figure=plot_map(pd.to_datetime('2022-02-03'), 10)
            )],width=8), 

         dbc.Col([ #column component within a row
             dbc.Row([ #row component within
                dcc.Markdown('**Weather**' + "\u2600"),
                html.Div([ #division component to group and structure other elements
                html.Span("Humidity: ", style={"font-weight": "bold"}),
                html.Span(id='humidity'), # specify id to reference the component dynamically from Dash callback function
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
            
    html.Hr(),  # Add a horizontal line as separator

            dbc.Row([ #row component within
            dcc.Markdown('**Depot events**' + "\U0001F389"),
            html.Div(id='event_title') #division component with specific ID, used to update the content dynamically   
        ]),

    html.Hr(),  # Add a horizontal line as separator

            dbc.Row([ #row component within
            dcc.Markdown('**Loko events**' + "\U0001F389"),
            html.Div(id='event_title2')            
        ]),

    html.Hr(),  # Add a horizontal line as separator

            dbc.Row([ #row component within
            dcc.Markdown('**School holidays**' + "\U0001F3EB"),
            html.Div(id='event_title3')            
        ]),

        ], style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}), # general style of events
    ])
], style={'background-color': '#ADD8E6'}) # background color of the app to #ADD8E6 - light blue color

## GENERAL COMMENT:
# dbc, dcc, and html modules are all part of the Dash library and are used to create different types of components for dash apps
# dbc (Dash Bootstrap Components): components and styles (Container, Row, Col, Navbar, Card)
# dcc (Dash Core Components):  highly customizable and interactive (Graph, Slider, DatePicker, Dropdown, Textarea, Input)
# html (HTML Components): low-level HTML components to be integrated in dash apps (Div, Span, H1, H2, P, Img, Button)

#----------------------------------------------------------------------------------------------------------

# Define the callback function to update the map based on the selected date and time 
# triggered when the input values change SO whenever 'date-picker' or 'hour-slider' components change
# specify the inputs and outputs of the callback function
@app.callback(Output('map-graph', 'figure'),
              Output('event_title', 'children'), #children bc it is a text content rendered within the component
              Output('event_title2', 'children'),
              Output('event_title3', 'children'),
              Output('humidity', 'children'),
              Output('rainin', 'children'),
              Output('temp_qcl3', 'children'),
              Input('date-picker', 'date'),
              Input('hour-slider', 'value'))

#----------------------------------------------------------------------------------------------------------

# function to update information based on date and time
# retrieves data from various sources to update the map, event titles, and weather information based on the selected date and hour
def update_map_and_event_and_weather(date, hour):

    selected_datetime = pd.to_datetime(date) #transform selected date to datetime

    #depot update
    event_data_depot = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/depot.csv') # data is loaded
    event_data_depot['StartDate'] = pd.to_datetime(event_data_depot['StartDate'])  # Convert StartDate to datetime type
    event_data_depot['EndDate'] = pd.to_datetime(event_data_depot['EndDate'])  # Convert EndDate to datetime type
    # event_data_depot is filtered based on the selected date using boolean indexing
    # It selects the rows where the 'StartDate' is <= to the selected date and the 'EndDate' is >= to the selected date
    # retrieve the event titles that fall within the selected date range and 
    # store them in the event_title variable and later convert to a list using tolist().
    event_title = event_data_depot[
        (event_data_depot['StartDate'].dt.date <= selected_datetime.date()) &
        (event_data_depot['EndDate'].dt.date >= selected_datetime.date())
    ]['Event Name'].tolist()

    #DO SAME FOR LOKO AND SCHOOL
    
    #loko update
    event_data_loko = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/events_loko.csv')
    event_data_loko['startdate'] = pd.to_datetime(event_data_loko['startdate'])  # Convert StartDate to datetime type
    event_data_loko['enddate'] = pd.to_datetime(event_data_loko['enddate'])  # Convert EndDate to datetime type
    event_title2 = event_data_loko[
        (event_data_loko['startdate'].dt.date <= selected_datetime.date()) &
        (event_data_loko['enddate'].dt.date >= selected_datetime.date())
    ]['event'].tolist()

    #school update
    event_data_school = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/school_holidays_belg.csv', encoding="mac_roman")
    event_data_school['StartDate'] = pd.to_datetime(event_data_school['StartDate'])  # Convert StartDate to datetime type
    event_data_school['EndDate'] = pd.to_datetime(event_data_school['EndDate'])  # Convert EndDate to datetime type
    event_title3 = event_data_school[
        (event_data_school['StartDate'].dt.date <= selected_datetime.date()) &
        (event_data_school['EndDate'].dt.date >= selected_datetime.date())
    ]['Holiday'].tolist()

    #weather update
    data = pd.read_csv('https://mda-noise.s3.eu-central-1.amazonaws.com/mergeddf01_df09.csv') #load data
    data['day'] = pd.to_datetime(data['day']) #convert day to datetime
    # select rows where the 'day' column is equal to the selected date and the 'start_hour' column is equal to the selected hour.
    selected_data = data[(data['day'] == date) & (data['start_hour'] == hour)]
    # variables are assigned with the values from the selected_data
    # filtering is performed based on the condition that the 'day' values are <= to the selected date
    # The values are converted to lists using tolist().
    humidity = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_HUMIDITY'].tolist()
    rainin = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_RAININ'].tolist()
    temp_qcl3 = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_TEMP_QCL3_list'].tolist()
    
    # figure to be displayed when selecting date and hour
    fig = plot_map(date, hour)
        
    #conditions for update to happen
    # for each variable, if data available (>0) it converts data to string and prints first set of characters
    # If there is no data available, it sets the variable to the string "No data (or events, holidays) on selected date/time".
    if len(humidity) > 0:
        humidity = str(humidity)[1:6]
    else:
        humidity = "No data on selected date/time"

    if len(rainin) > 0:
        rainin = rainin[0] 
    else:
        rainin = "No data on selected date/time"

    if len(temp_qcl3) > 0:
        temp_qcl3 = str(temp_qcl3)[1:5]
    else:
        temp_qcl3 = "No data on selected date/time"

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

    # values to display in the app
    return fig, event_title, event_title2, event_title3, humidity, rainin, temp_qcl3

#----------------------------------------------------------------------------------------------------------

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True) #enables debug mode so it gives you info and error messages - makes it easier in development phase 
    
#COMMENTS

# this code checks if the current script is being run as the main module. It ensures that the following code is only executed when the script is executed directly and not when it is imported as a module in another script.

# app.run_server(debug=True) is the code that runs the Dash application server. By including this code within the if __name__ == '__main__': block, it ensures that the server is started only when the script is executed directly.

