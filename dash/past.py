import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from datetime import date, timedelta

# Define the function to plot the map
def plot_map(date, hour):

    # Load the dataset with noise data
    data = pd.read_csv('mergeddf01_df09.csv')

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

    dbc.Row([
        dbc.Col([
            dcc.Markdown('**Date** \U0001F4C5',
                         style={'font-weight': 'bold', 'font-size': '20px', 'font-style': 'italic'}),
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
              Input('date-picker', 'date'),
              Input('hour-slider', 'value'))

# function to update information based on date and time
def update_map_and_event_and_weather(date, hour):

    selected_datetime = pd.to_datetime(date)

    #depot update
    event_data_depot = pd.read_csv('depot.csv')
    event_data_depot['StartDate'] = pd.to_datetime(event_data_depot['StartDate'])  # Convert StartDate to datetime type
    event_data_depot['EndDate'] = pd.to_datetime(event_data_depot['EndDate'])  # Convert EndDate to datetime type
    event_title = event_data_depot[
        (event_data_depot['StartDate'].dt.date <= selected_datetime.date()) &
        (event_data_depot['EndDate'].dt.date >= selected_datetime.date())
    ]['Event Name'].tolist()

    #loko update
    event_data_loko = pd.read_csv('loko.csv')
    event_data_loko['startdate'] = pd.to_datetime(event_data_loko['startdate'])  # Convert StartDate to datetime type
    event_data_loko['enddate'] = pd.to_datetime(event_data_loko['enddate'])  # Convert EndDate to datetime type
    event_title2 = event_data_loko[
        (event_data_loko['startdate'].dt.date <= selected_datetime.date()) &
        (event_data_loko['enddate'].dt.date >= selected_datetime.date())
    ]['event'].tolist()

    #school update
    event_data_school = pd.read_csv('holidays.csv', encoding="mac_roman")
    event_data_school['StartDate'] = pd.to_datetime(event_data_school['StartDate'])  # Convert StartDate to datetime type
    event_data_school['EndDate'] = pd.to_datetime(event_data_school['EndDate'])  # Convert EndDate to datetime type
    event_title3 = event_data_school[
        (event_data_school['StartDate'].dt.date <= selected_datetime.date()) &
        (event_data_school['EndDate'].dt.date >= selected_datetime.date())
    ]['Holiday'].tolist()

    #weather update
    data = pd.read_csv('mergeddf01_df09.csv')
    data['day'] = pd.to_datetime(data['day'])
    selected_data = data[(data['day'] == date) & (data['start_hour'] == hour)]
    humidity = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_HUMIDITY'].tolist()
    rainin = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_RAININ'].tolist()
    temp_qcl3 = selected_data[(selected_data['day'].dt.date <= selected_datetime.date())]['LC_TEMP_QCL3_list'].tolist()
    
    fig = plot_map(date, hour)
        
    #conditions for update to happen
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

    return fig, event_title, event_title2, event_title3, humidity, rainin, temp_qcl3

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
