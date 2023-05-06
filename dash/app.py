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
    data = pd.read_excel('test1.xlsx',parse_dates=['date'])
    #print(data)
    # Filter the dataset to include only the rows with the specified date and hour
    filtered_data = data[(data['date'] == date) & (data['time'] == hour)]
    #print(filtered_data)
    
    # Set the mapbox access token
    mapbox_access_token = 'pk.eyJ1IjoiY2hpYW0wMzgiLCJhIjoiY2xnemFpODRrMGhqOTNwb2d6ZHF4MGN4aiJ9.TNlviVcT53vGInxiKM-vxQ'

    # Define the layout of the map using Mapbox
    layout = go.Layout(
        mapbox=dict(
            accesstoken=mapbox_access_token,
            style='mapbox://styles/mapbox/light-v10', # Set the style of the map
            center=dict(lon=4.701187398271877, lat=50.87906486209482), # Set the center of the map to the town hall
            zoom=14, # Set the zoom level of the map
            ),
        )
    
     # Check if there is any data in the filtered_data dataframe
    if not filtered_data.empty:
        # Define the data for the map
        lon = filtered_data['lon'] # Longitude of each point
        lat = filtered_data['lat'] # Latitude of each point
        noise = filtered_data['noise'].fillna(0) # Replace missing values with 0
        name = filtered_data['name']
        
        # Calculate the sizeref value based on non-zero values of noise
        if noise.any():
            sizeref = np.array(noise.dropna()).max() / 20
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
                sizeref= sizeref,
                color='blue'
            ),
            hovertemplate='<b>%{text}</b><br>Noise: %{marker.size}<extra></extra>',
            text=name
        )
    
        # Create the map with go.Scattermapbox
        fig = go.Figure(data=trace, layout=layout)
    
    else:
        # Define an empty trace with mode='text'
        trace = go.Scattermapbox(
            lat=[],
            lon=[],
            mode='text',
            text='',
        )

        # If there is no data in the filtered_data dataframe, create an empty map
        fig = go.Figure(data=trace, layout=layout)
    
    # Update the layout of the map with Mapbox-specific settings
    fig.update_layout(layout,height=800)
    
    # Show the map
    return fig

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
                dcc.Markdown('Noise and Event in Naamsestraat Leuven',style={'textAlign':'center'})
        ],width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Markdown('Date'),
            dcc.DatePickerSingle(
            id='date-picker',
            min_date_allowed=date(2022, 1, 1),
            max_date_allowed=date(2022, 12, 1),
            date=date(2022, 1, 1)
            )    
        ],width=6),
        
        dbc.Col([
            dcc.Markdown('Time'),
            hour := dcc.Input(id='hour',type='number',value=10,min=0,max=23)
        ],width=6)        
    ]),
    
    dbc.Row([
        dbc.Col([
        dcc.Graph(
            id='map-graph',
            figure=plot_map(pd.to_datetime('2022-02-03'), 10)
        )],width=12) 
    ])
])

# Define the callback function to update the map based on the selected date and time
@app.callback(Output('map-graph', 'figure'),
              Input('date-picker', 'date'),
              Input('hour', 'value'))
def update_map(date, hour):
    selected_datetime = pd.to_datetime(date)
    hour=hour
    return plot_map(selected_datetime, hour)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)