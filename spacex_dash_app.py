# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                ],
                                value='ALL',
                                placeholder = 'Select a launch site',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 1000:'1000', 2000:'2000', 3000:'3000',
                                                4000:'4000', 5000:'5000', 6000:'6000', 7000:'7000',
                                                8000:'8000', 9000:'9000', 10000: '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(chosen_site):
    if (chosen_site == 'ALL'):
        data = spacex_df
        fig = px.pie(data, values='class',
        names='Launch Site',
        title='Successful Launch Breakdown')
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == chosen_site]
        filtered_df['result'] = filtered_df['class'].map(lambda x: 'Success' if x==1 else 'Failure')
        filtered_df['sum_class'] = filtered_df['class'].map(lambda x: 1)
        data = filtered_df
        fig = px.pie(data, values='sum_class',
        names='result',
        title=f'Successful Launch Breakdown for {chosen_site}')    

    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'), 
             [Input(component_id='site-dropdown', component_property='value'), 
             Input(component_id='payload-slider', component_property='value')])
def render_scatter_plot(chosen_site, masses):
    data = spacex_df
    pay_min = masses[0]
    pay_max = masses[1]
    spacex_df['Booster Version Category'] = spacex_df['Booster Version'].map(
        lambda x: x.split()[1]
    )
        
    f1_df = spacex_df.loc[spacex_df['Payload Mass (kg)'] <= pay_max]
    f2_df = f1_df.loc[f1_df['Payload Mass (kg)'] >= pay_min]
    data = f2_df

    if(chosen_site == 'ALL'):
        fig = px.scatter(data, x='Payload Mass (kg)', y='class', 
        color='Booster Version Category',
        title='All Sites Payload Mass Results')
    else:
        filtered_df = spacex_df.loc[spacex_df['Launch Site'] == chosen_site]
        data = filtered_df
        fig = px.scatter(data, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title=f'{chosen_site} Payload Mass Results')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()

# 1. VAFB Has the single largest successful launch
# 2. CCAFS SLC-40 has the highest success rate of launches
# 3. 2000 - 4000 kg has the highest success rate in terms of payload
# 4. 6000 - 8000 kg has the lowest success rate in terms of payload
# 5. Technically B5 has the highest success rate