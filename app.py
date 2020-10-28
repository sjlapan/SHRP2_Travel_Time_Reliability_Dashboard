import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import sys
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import os
import time
import json

# from flask_caching import Cache
# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# Step 1. Launch the application
dirname = os.path.dirname(__file__)

app = dash.Dash(
    __name__, 
)

server = app.server

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Step 2. Import the data set
filename = os.path.join(dirname, "Data","data.csv")
# img_file = 'navjoy-logo.jpg'#os.path.join(dirname, "Assets", 'navjoy-logo.png')
# cdot_img_file = 'cdot_logo.jpg' #os.path.join(dirname, "Assets", 'cdot_logo.png')
df = pd.read_csv(filename)

df = df[[
    "road",
    "f_system",
    "urban_rural",
    "class",
    "year",
    "date_time",
    "day_string",
    "interval",
    "travel_time_minutes",
    "baseline_mean_TT",
    "percent_change",
    "impact_type",
    "impact_subtype",
    "corridor_response"
]]

df.interval = pd.to_datetime(
            df["interval"], 
            format= "%H:%M"
            ).dt.hour
# Set up functions
def string_converter(input_list, separater):
    if len(input_list) == 1:
        final_string = input_list[0]
    else:
        final_string = separater.join(input_list)
    return final_string


# Used for graph colors (maybe)
hexcodes = [
    "",
    "#00E5C4",
    "#01E5D8",
    "#02DEE6",
    "#03CBE6",
    "#04B8E7",
    "#06A5E7",
    "#0791E8",
    "#087FE8",
    "#096CE9",
    "#0B59E9",
    "#0C47EA",
    "#0D34EA",
    "#0E22EB",
    "#1010EB",
    "#2411EC",
    "#3812EC",
    "#4D14ED",
    "#6115EE",
    "#7516EE",
    "#8917EF",
    "#9C19EF",
    "#B01AF0",
    "#C41BF0",
    "#D71DF1",
    "#EA1EF1",
    "#F21FE6",
    "#F221D5",
    "#F322C3",
    "#F324B1",
    "#F425A0",
    "#F4268F",
    "#F5287E",
    "#F5296D",
    "#F62A5C",
    "#F72C4B",
    "#F72D3B",
    "#F8332F",
    "#F84630",
    "#F95932",
    "#F96B33",
    "#FA7E34",
    "#FA9036",
    "#FBA337",
    "#FBB539",
    "#FCC63A",
    "#FCD83C",
    "#FDEA3D",
    "#FDFB3F",
    "#F0FE40",
    "#DFFF41",
]

# Initialize Table values to match values shown on other graphs

# Used for the impact type dropdown
impact_type_list = [
    "All",
    "Work Zone",
    "Incident",
    "Weather",
    "Special Event"
]

# Used to initialize the impact subtype dropdown
default_subtype_list = [
    "All"
]

# Used to intialize the corridor ID dropdown 
default_cor_ID_list = [
    "all"
]

# List of years to filter for
year_list = [
    "All",
    "2017",
    "2018",
    "2019"
]

# Used for the weekday dropdown
weekday_list = [
    "All",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

# Used for the lane closure dropdown
corridor_response_dropdown_list = [
    "All",
    "No information",
    "No closure",
    "Partial closure", 
    "All lanes closed",
    "On-ramp or off-ramp closure",
    ]

# Used to update the impact subtype list for WZ
work_zone_subtype_dropdown_list = [
    "All",
    "Paving operations",
    "Striping Operations",
    "Road construction",
    "Road maintenance",
    "Signal work",
 
    ]

# Used to update the impact subtype list for Inc
incident_subtype_dropdown_list = [
    "All",
    "Accident - multi vehicle",
    "Accident - single vehicle",
    "Mechanical",
    "Spun out/slide off",
    ]

# Used to update the impact subtype list for wthr
weather_subtype_dropdown_list = [
    "All",
    "Winter storm",
    "Blizzard",
    "Snow",
    "Hail",
    "Ice storm",
    "Ice glaze",
    "Rain and snow mixed",
    "Thunder storms",
    "Strong winds",
    "Hurricane force winds",
    "Tornado",
    "Severe weather",
    "Heavy rain",
    "Fog"
    ]

# Used to update the impact subtype list for events
special_event_subtype_dropdown_list = [
    "All",
    "Sporting event",
    "Holiday traffic",
    "Funeral procession",
    "Festival",
    "Concert",
    "Parade",
    "Procession",
    "VIP visit"
]

# Dictionary for chart labels

label_dict = {
    'f_system': 'Corridor Type',
    'class': 'Corridor Subtype',
    'urban_rural': "Urban Class",
    'impact_type': 'Impact Type',
    'impact_subtype': 'Impact Subtype',
    'corridor_response': 'Lane Closure(s)' 
}

# Used to initialize the list of options for the second chart variable
second_variable_dict = {
    "None": "none",
    "Urban Class": "urban_rural",
    "Impact Type": 'impact_type',
    "Impact Subtype": 'impact_subtype',
    "Lane Closure(s)": 'corridor_response'
}

# Updated options if first variable = corridor subtype 
corr_sub_dict = {
    "None": "none",
    "Impact Type": 'impact_type',
    "Impact Subtype": 'impact_subtype',
    "Lane Closure(s)": 'corridor_response'
}

# Updated options if first variable = impact type
imp_dict = {
    "None": "none",
    "Urban Class": "urban_rural",
    "Impact Subtype": 'impact_subtype',
    "Lane Closure(s)": 'corridor_response'
}

# Updated options if first variable = impact subtype
imp_sub_dict = {
    "None": "none",
    "Lane Closure(s)": 'corridor_response'
}

# Updated options if first variable = Lane Closure(s)
closure_dict = {
    "None": "none"
}

# Step 3. Create Dash layout.

app.layout = html.Div(
children=[
        html.Div(
            className="row",
            children=[

                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    # Add CDOT logo (and SHRP2 logo)
                    children=[

                        # html.Img(
                        #     # className="logo", 
                        #     src=app.get_asset_url('cdot_logo.jpg'),
                        #     alt= 'CDOT Logo',
                        #     style = {
                        #         'height': 719,
                        #         'width': 152
                        #     }
                        # ),
                        
                        # html.Img(
                        #     # className="logo", 
                        #     src=app.get_asset_url('navjoy-logo.jpg'),
                        #     alt= 'Navjoy Logo',
                        #     style = {
                        #         'height': 719,
                        #         'width': 152
                        #     }
                        # ),

                        html.H1("SHRP2 Travel Time Reliability"),
                        
                        html.P(
                            """Explore and compare the impact of various nonrecurring sources of congestion 
                            on vehicle travel times in Colorado (measured as the percent change in travel 
                            time compared to normal conditions). For source code and additional information 
                            regarding this project, click <a href = 'https://github.com/sjlapan/SHRP2_Travel_Time_Reliability_Dashboard/'>here</a>.
                            """
                        ),

                        html.H3("Variables"),
                        
                        html.P(
                            """Select your first parameter."""
                        ),

                        dcc.Dropdown(
                            options = [
                                {'label': 'Corridor Type', 'value': 'f_system'},
                                {'label': 'Corridor Subtype', 'value': 'class'},
                                {'label': 'Impact Type', 'value': 'impact_type'},
                                {'label': 'Impact Subtype', 'value': 'impact_subtype'},
                                {'label': 'Lane Closure(s)', 'value': 'corridor_response'},
                                {'label': 'Time of Day', 'value': 'interval'},
                            ],
                            id="param-1",
                            value='f_system'
                        ),

                        html.P(
                            """
                            Select your first time interval.
                            """,
                            id= "interval-one-label",

                            style={'display': 'none'}
                        ),

                        # Set default values for these sliders. Lists?
                        html.Div(
                            dcc.RangeSlider(
                                min= 0,
                                max=23,
                                step=1,
                                marks = {
                                    0: '0:00',
                                    # 1: '1',
                                    # 2: '2:00',
                                    # 3: '3:00',
                                    # 4: '4:00',
                                    # 5: '5',
                                    6: '6:00',
                                    # 7: '7',
                                    # 8: '8',
                                    # 9: '9:00',
                                    # 10: '10',
                                    # 11: '11',
                                    12: '12:00',
                                    # 13: '13',
                                    # 14: '14',
                                    # 15: '15:00',
                                    # 16: '16',
                                    # 17: '17',
                                    18: '18:00',
                                    # 19: '19',
                                    # 20: '20',
                                    # 21: '21:00',
                                    # 22: '22',
                                    23: '23:00',
                                },
                                tooltip = {
                                    'placement': 'top',
                                },
                                id= "interval-selector-one",
                                value=[6,9]
                                
                            ),
                            style={'display': 'none'},
                            id= 'first-interval-div'
                        ),

                        html.P(
                            """
                            Select your second time interval.
                            """,
                            id= "interval-two-label",

                            style={'display': 'none'}
                        ),
                        html.Div(
                            dcc.RangeSlider(
                                min= 0,
                                max=23,
                                step=1,
                                marks = {
                                    0: '0:00',
                                    # 1: '1',
                                    # 2: '2:00',
                                    # 3: '3:00',
                                    # 4: '4:00',
                                    # 5: '5',
                                    6: '6:00',
                                    # 7: '7',
                                    # 8: '8',
                                    # 9: '9:00',
                                    # 10: '10',
                                    # 11: '11',
                                    12: '12:00',
                                    # 13: '13',
                                    # 14: '14',
                                    # 15: '15:00',
                                    # 16: '16',
                                    # 17: '17',
                                    18: '18:00',
                                    # 19: '19',
                                    # 20: '20',
                                    # 21: '21:00',
                                    # 22: '22',
                                    23: '23:00',
                                },
                                tooltip = {
                                    'placement': 'top',
                                },
                                id= "interval-selector-two",
                                value=[16,19]
                            ),
                            style={'display': 'none'},
                            id= 'second-interval-div',
                            
                ),

                        html.P(
                            """Select your second parameter."""
                        ),

                        dcc.Dropdown(
                            options = [
                                {'label': key, 'value': value} for key, value in second_variable_dict.items()
                            ],
                            id="param-2",
                            value='none'
                        ),
                        
                        html.H3("Filters (Optional)"),

                        html.P(
                            """Apply filters to the data to improve performance
                            and refine your search."""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[

                                html.Label('Impact Type'),

                                dcc.Dropdown(
                                    options=[
                                        {'label': name, 'value': name.lower()} for name in impact_type_list
                                    ],
                                    id="impact-filter",
                                    multi=True,
                                    value="all"
                                ),

                                html.Label('Impact Subtype'),

                                dcc.Dropdown(
                                    options=[
                                        {'label': name, 'value': name} for name in default_subtype_list
                                    ],
                                    id="impact-sub-filter",
                                    value= "all",
                                    multi= True,
                                ),

                                html.Label('Corridor Type'),

                                dcc.Dropdown(
                                    options=[
                                        {'label': 'All', 'value': 'all'},
                                        {'label': 'Interstate', 'value': 'Interstate'},
                                        {'label': 'Freeway', 'value': 'Freeway'},
                                        {'label': 'Highway', 'value': 'Highway'}
                                    ],
                                    value='all',
                                    multi=True,
                                    id="corridor-filter"
                                ),

                                html.Label('Terrain'),

                                dcc.RadioItems(
                                    options=[
                                        {'label': 'All', 'value': 'all'},
                                        {'label': 'Urban', 'value': 'Urban'},
                                        {'label': 'Rural', 'value': 'Rural'},
                                
                                    ],
                                    id="terrain-filter",
                                    value='all'
                                ),

                                html.Label('Lane Closure(s)'),
                                dcc.Dropdown(
                                    options=[
                                        {'label': name, 'value': name.lower()} for name in corridor_response_dropdown_list
                                    ],
                                    
                                    multi=True,
                                    id="closure-filter",
                                    value='all'
                                ),
                                
                                html.Div(
                                    children=[
                                        html.Label('Corridor ID'),
                                        dcc.Dropdown(
                                            options=[
                                                {'label': name, 'value': name} for name in default_cor_ID_list
                                            ],
                                            
                                            multi=True,
                                            id="corridor-ID-filter",
                                            value='All',
                                        ),
                                        html.Button('Refresh Corridor List', id='road-refresh', n_clicks=0)
                                    ]
                                ),
                                html.Label('Year(s)'),
                                dcc.Dropdown(
                                    options=[
                                        {'label': name, 'value': name.lower()} for name in year_list
                                    ],
                                    
                                    multi=True,
                                    id="year-filter",
                                    value='all'
                                ),

                                html.Label('Weekday(s)'),
                                dcc.Dropdown(
                                    options=[
                                        {'label': 'All', 'value': 'all'},
                                        {'label': 'Monday', 'value': 'Monday'},
                                        {'label': 'Tuesday', 'value': 'Tuesday'},
                                        {'label': 'Wednesday', 'value': 'Wednesday'},
                                        {'label': 'Thursday', 'value': 'Thursday'},
                                        {'label': 'Friday', 'value': 'Friday'},
                                        {'label': 'Saturday', 'value': 'Saturday'},
                                        {'label': 'Sunday', 'value': 'Sunday'},
                                    ],
                                    multi=True,
                                    id="weekday-filter",
                                    value='all'
                                ),
                            ],
                        ),

                        html.Button("Apply Filters", id="filter-submit", n_clicks=0),

                        html.P(
                            id='filter-message',
                            children=""" """
                        ),
                        
                    ],
                ),

                # Column for app graphs and plots

                html.Div(
                    id='output',
                    style={'display': 'none'},
                    children=df.to_json(),
                ),

                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        
                        dcc.Loading(
                            id='loading-1',
                            children = [
                                dcc.Graph(
                                    id='violin-graph',
                                    figure={}
                                ),
                                ],
                            type= 'circle'
                        ),
                                              
                        # html.Div(
                        #     className="text-padding",
                        #     children=[
                        #         " "
                        #     ],
                        # ),

                        dcc.Loading(
                            id='loading-4',
                            children = [

                                dcc.Graph(    
                                    id='table',
                                    figure={},
                                    style={'height': 250 }
                                ),
                            ],
                            type= 'circle'
                        ),

                        html.Div(
                            className="text-padding",
                            children=[
                                " "
                            ],
                        ),

                        dcc.Loading(
                            id='loading-2',
                            children = [
                                dcc.Graph(
                                    id='cdf-graph',
                                    figure={}
                            ),
                            ],
                            type= 'circle'
                        ),

                        html.Div(
                            className="text-padding",
                            children=[
                                " "
                            ],
                        ),

                        html.Div(
                            className="text-padding",
                            children=[
                                " "
                            ],
                        ),

                        dcc.Loading(
                            id='loading-3',
                            children = [
                                dcc.Graph(
                                    id='example-graph',
                                    figure={}
                                ),
                            ],
                            type= 'circle'
                        ),

                        html.Div(
                            className="text-padding",
                            children=[
                                " "
                            ],
                        ),
                        
                        html.P(
                            "Developed by Navjoy in partnership with Colorado Department of Transportation"
                        )

                    ],
                ),
            ],
        )
    ]

)

# Step 4. Add callback functions

# Function for triggering the time interval selection options
@app.callback(
    [
        Output(component_id = 'interval-one-label', component_property= 'style'),
        Output(component_id = 'first-interval-div', component_property= 'style'),
        Output(component_id = 'interval-two-label', component_property= 'style'),
        Output(component_id = 'second-interval-div', component_property= 'style'),
    ],
    Input(component_id='param-1', component_property='value')
)
def slider_activation(option_slctd):
    if option_slctd == 'interval':
        return [
            {'display':'inline'},
            {'display':'inline'},
            {'display':'inline'},
            {'display':'inline'},
        ]
    else:
        return [
            {'display': 'none'},
            {'display': 'none'},
            {'display': 'none'},
            {'display': 'none'},
        ]

# Function for updating the impact subtype list 
# based on the Impact Type selection
@app.callback(
    Output(component_id='impact-sub-filter', component_property='options'),
    Input(component_id='impact-filter', component_property='value')
)
def update_sublist(option_slctd):
    opt_list = ["All"]
    # print(option_slctd)
    if option_slctd == "all":
        opt_list = ["All"]
    elif option_slctd == ["work zone"]:
        opt_list = work_zone_subtype_dropdown_list
    elif option_slctd == ["incident"]:
        opt_list = incident_subtype_dropdown_list
    elif option_slctd == ["weather"]:
        opt_list = weather_subtype_dropdown_list
    elif option_slctd == ["special event"]:
        opt_list = special_event_subtype_dropdown_list
    return [{'label': i, 'value': i.lower()} for i in opt_list]


# Function for updating the corridor ID list.
@app.callback(
Output(component_id='corridor-ID-filter', component_property='options'),
Input(component_id='road-refresh', component_property='n_clicks'),
state=[
    State(component_id='output', component_property='children')
]
)
def update_road_list(button, dataframe):
    # print(f'here it is: {dataframe}')
    # Reinitialize the corridor ID list
    default_cor_ID_list = [
        "All"
    ]
    if dataframe != None:
        df = pd.read_json(dataframe)
        # print(df.head())
        corridors = df.road.value_counts().index.tolist()
        # print(corridors)
        default_cor_ID_list.extend(corridors)
        # print(default_cor_ID_list)
        return [{'label': i, 'value': i} for i in default_cor_ID_list]


# Function for filtering the dataframe
@app.callback(
    [
        Output(component_id='output', component_property="children"),
        Output(component_id='example-graph', component_property='figure'),
        Output(component_id='filter-message', component_property='children')
    ],
    [
        Input(component_id='filter-submit', component_property='n_clicks'),
    ],
    state=[
        State(component_id='impact-filter', component_property='value'),
        State(component_id='impact-sub-filter', component_property='value'),
        State(component_id='corridor-filter', component_property='value'),
        State(component_id='terrain-filter', component_property='value'),
        State(component_id='closure-filter', component_property='value'),
        State(component_id='corridor-ID-filter', component_property='value'),
        State(component_id='year-filter', component_property='value'),
        State(component_id='weekday-filter', component_property='value')
        ]    
) 
def filter_df(
            button,

            imp_option_slctd, 
            sub_opt_slctd, 
            cor_slctd, 
            trrn_slctd, 
            cls_slctd,
            id_slctd,
            yr_slctd,
            wkd_slctd
            ): 
    # print(imp_option_slctd)
    input_dict={}

    input_dict = {
            'impact_type': imp_option_slctd, 
            'impact_subtype': sub_opt_slctd, 
            'f_system': cor_slctd, 
            'urban_rural': trrn_slctd, 
            'corridor_response': cls_slctd,
            "road": id_slctd,
            "year": yr_slctd,
            "day_string": wkd_slctd
        }
   
    # Reinitialize the dataframe and your filter dictionary
    active_filter_dict = {}
    filtered_df = df.copy()
    
    error_string = ''
    error_items = []
    # Tracks button clicks.

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    print(changed_id)

    # Triggers filter sequence when the Apply Filters button is clicked.
    if 'filter-submit' in changed_id:        

        # Reinitialize the dataframe and your filter dictionary
        active_filter_dict = {}
        filtered_df = df.copy()
        
        # Working out error handling for bad filters
        error_string = ''
        error_items = []
        # Look for any inputs that have a filter parameter applied
        for key, value in input_dict.items():
            if value not in ['All', 'all',['All'], ['all']]:
                active_filter_dict[key]= value
            else:
                continue
        print(active_filter_dict)
        # Checks to see if any filters are applied
        if len(active_filter_dict) > 0:
            for key, value in active_filter_dict.items():
                # Checks to see if more than one value is given as a parameter
                if isinstance(value, list) == True:
                    # Checks to make sure you don't filter out all data points
                    if len(filtered_df[filtered_df[key].isin(value)]) > 0:
                        filtered_df = filtered_df[filtered_df[key].isin(value)]
                        # print(f"New length: {len(filtered_df)}")
                        # print(filtered_df[key].value_counts())
                    else:
                        print(f"Your filter for {string_converter(error_items, ', ')} returned zero results, and was not applied")
                        if value not in ['All', 'all']:
                            error_items = error_items + value
                            # print("This is error items if the filter is a list and len is 0:")
                            # print(error_items)
                        continue
                else:
                    # Checks to make sure you don't filter out all data points
                    if len(filtered_df[filtered_df[key] == value]) > 0:
                        filtered_df = filtered_df[filtered_df[key] == value]
                        # print(f"New length: {len(filtered_df)}")
                    else:
                        # print(f"Your filter for {value} returned zero results, and was not applied")
                        if value not in ['All', 'all']:
                            error_items.append(value)
                            # print("This is error items if the filter is NOT a list and len is 0:")
                            # print(error_items)
                        continue

            # print(f'Filtered dataframe length: {len(filtered_df)}')
        else:
            print(f'Full dataframe length: {len(filtered_df)}')

        # Repopulate the histogram
        fig1 = px.histogram(
            filtered_df, 
            x="road"
        )
        fig1.update_xaxes(title_text = "Corridor")
        fig1.update_yaxes(title_text = "Count")
        fig1.update_layout(title_text = "Count of Data Points by Corridor")

        if len(error_items) >0:
            error_string = f'Your filter for {string_converter(error_items, ", ")} returned zero results, and was not applied.'
        else:
            error_string = ' '
        return filtered_df.to_json(), fig1, error_string
    else:
        # Resets dataframe. Then populate histogram with unfiltered data.
        filtered_df = df.copy()
        error_string = ' '
        fig1 = px.histogram(
                filtered_df, 
                x="road"
            )
        fig1.update_xaxes(title_text = "Corridor")
        fig1.update_yaxes(title_text = "Count")
        fig1.update_layout(title_text = "Count of Data Points by Corridor")
    # Return your dataframe jsonified, and your figure
    return filtered_df.to_json(), fig1, error_string

# Function for updating your list of options for parameter 2
# based on the user selection for parameter 1.

@app.callback(
    Output(component_id='param-2', component_property='options'),
    Input(component_id='param-1', component_property='value')
)
def update_param_2(option_slctd):
    opt_dict = second_variable_dict
    if option_slctd == "f_system":
        opt_dict = second_variable_dict
    elif option_slctd == "class":
        opt_dict = corr_sub_dict
    elif option_slctd == "impact_type":
        opt_dict = imp_dict
    elif option_slctd == "impact_subtype":
        opt_dict = imp_sub_dict
    elif option_slctd == "corridor_response":
        opt_dict = closure_dict
    elif option_slctd == "hour":
        opt_dict = second_variable_dict

    # Repopulate the dropdown
    return [{'label': key, 'value': value} for key, value in opt_dict.items()]

# Function to generate violin plot, table, and CDF plot.
@app.callback(
    [
        Output(component_id='violin-graph', component_property= 'figure'),
        Output(component_id='cdf-graph', component_property= 'figure'),
        Output(component_id='table', component_property='figure')
    ],
    [
        Input(component_id= 'output', component_property="children"),
        Input(component_id= 'param-1', component_property= 'value'),
        Input(component_id= 'param-2', component_property= 'value'),
        Input(component_id= 'interval-selector-one', component_property= 'value'),
        Input(component_id= 'interval-selector-two', component_property= 'value'),
    ]
)
def generate_plots(
                    dataframe, 
                    inp_1, 
                    inp_2, 
                    time_1, 
                    time_2
                    ):
    # Read in your jsonified dataframe
    df2 = pd.read_json(dataframe)
    
    stat_labels = [
        "Mean",
        "SD",
        "Min",
        "25% (Q1)",
        "Median",
        "75% (Q3)",
        "Max"
    ]

    # header_list = ["Measure"]
    header_list = [" "]
    stats_list = [stat_labels]
    # Assign your inputs to variables.    
    if inp_1 != "interval":
        x_axis_variable = inp_1
        x_category = label_dict[inp_1]
    else:
        print('It is time interval time')
        print(time_1)
        period_1_start = time_1[0]
        period_1_end = time_1[1]
        period_2_start = time_2[0]
        period_2_end = time_2[1]

        # subset the dataframe
        df2 = df2[
            (df2.interval >= period_1_start) &
            (df2.interval <= period_1_end) |
            (df2.interval >= period_2_start) &
            (df2.interval <= period_2_end)
            ]

        df2["time_range"] = ""
        df2.loc[
            (df2.interval >= period_1_start) &
            (df2.interval <= period_1_end), "time_range"
            ] = f"{period_1_start}:00 - {period_1_end}:00"

        df2.loc[
            (df2.interval >= period_2_start) &
            (df2.interval <= period_2_end), "time_range"
            ] = f"{period_2_start}:00 - {period_2_end}:00"
        x_axis_variable = "time_range"
        x_category = "Time of Day"
    
    # Initialize figures
    box_fig = go.Figure()
    cdf_fig = go.Figure()
    # table = go.Figure()

    # Generates plots using both variables
    if inp_2 != "none":
        color_variable = inp_2
        color_category = label_dict[inp_2]
        # Violin Plot
        for i, color in enumerate(df2[color_variable].unique()):
            
            box_fig.add_trace(go.Violin(
                x=df2[x_axis_variable][df2[color_variable] == color],
                y=df2["percent_change"][df2[color_variable] == color],
                name = color,
                box_visible=True,
                meanline_visible=True,                    
                ))

        box_fig.update_layout(violinmode="group")   
        box_fig.update_yaxes(title_text = "Percent Change (%)")
        box_fig.update_layout(title_text = f"Percent Change in Travel Time by" \
            f" {x_category} and {color_category}",                      
            )
        box_fig.update_layout(
            margin=go.layout.Margin(
                # t=2,
                b=2
            )
        )

        # CDF Plot
        for i, category in enumerate(df2[x_axis_variable].unique()):    
            for j, color in enumerate(
                    df2[color_variable][df2[x_axis_variable] == category].unique()
                    ):

                sub_df = df2[(df2[color_variable] == color) &
                    (df2[x_axis_variable] == category)
                    ]

                x = np.sort(sub_df["percent_change"])               
                
                y = np.arange(1, len(x) + 1)/(float(len(x)))
                cdf_fig.add_trace(go.Scatter(
                    mode="lines",
                    connectgaps=True,
                    x=x,
                    y=y,
                    hovertemplate="Percent Change (%): %{x} <br> Cumulative" \
                        " Probability: %{y}",
                    name= f"{category}, {color}",
                    ))

                header_list.append(str(category).title()+", " + str(color).title())

                stats =sub_df.percent_change.describe().tolist()
                stats = [round(elem, 2) for elem in stats]

                stats_list.append(stats[1:])
                # print(stats_list)
                # Table stuff here

    # Generates plots with only one variable selected
    elif inp_2 == "none":

        box_fig.add_trace(go.Violin(
            x=df2[x_axis_variable],
            y=df2["percent_change"],
            box_visible=True,
            meanline_visible=True,  
            )
        )

        box_fig.update_layout(violinmode="group")
       
        box_fig.update_yaxes(title_text = "Percent Change (%)")

        box_fig.update_layout(title_text = f"Percent Change in Travel Time" \
            f" by {x_category}"
            )
        box_fig.update_layout(
            margin=go.layout.Margin(
                # t=2,
                b=2
            )
        )

        for i, category in enumerate(df2[x_axis_variable].unique()):

            x= np.sort(df2["percent_change"][df2[x_axis_variable] == category])
            y = np.arange(1, len(x) + 1)/(float(len(x)))
            
            cdf_fig.add_trace(go.Scatter(
                mode="lines",
                connectgaps=True,
                x=x,
                y=y,
                hovertemplate="Percent Change (%): %{x} <br> Cumulative" \
                    " Probability: %{y}",
                name= category,         
                ))

            header_list.append(str(category.title()))
            sub_df = df2[df2[x_axis_variable] == category]
            stats = sub_df.percent_change.describe().tolist()
            stats = [round(elem, 2) for elem in stats]
            stats_list.append(stats[1:])
            # print(stats_list)

    # Generate New Table
    table_df = pd.DataFrame(stats_list)
    table_df = table_df.transpose()
    table_df.columns = header_list
    
    table_header = table_df.columns
    table_data = table_df.transpose().values.tolist()
    # Render your table df

    table = go.Figure(data=[
        go.Table(
            header=dict(
                values=[f'<b>{header}</b>' for header in list(table_df.columns)]
            ),
            cells = dict(
                values=table_df.transpose().values.tolist()
            )
        )
    ])

    if len(table_header) <15:
        fontsize = 12
    elif len(table_header) < 27:
        fontsize = 8
    elif len(table_header) < 30:
        fontsize = 6
    else:
        fontsize = 4
    
    table.update_layout(
        margin=go.layout.Margin(
            # l=5,
            # r=2,
            b=0,
            t=2,
            pad=0
        ),
        autosize=True,
        font=dict(
            size=fontsize
        )


    )

    cdf_fig.update_yaxes(tick0 = 0.0, dtick = 0.05)

    cdf_fig.update_xaxes(title_text = "Percent Change in Travel Time (%)")

    cdf_fig.update_yaxes(title_text = "Cumulative Distribution Value (%)")

    cdf_fig.update_layout(title_text = f"Cumulative Distribution Functions of" \
        f" Percent Change in Travel Time by {x_category}")
        
    return box_fig, cdf_fig, table


# Step 5. Add the server clause

if __name__ == '__main__':
    app.run_server(debug=False)