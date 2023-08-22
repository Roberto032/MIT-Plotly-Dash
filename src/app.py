import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime

df = pd.read_csv('EXAMPLEDATA1.csv')

app = dash.Dash()
server = app.server
year_options = [{'label': 'All Years', 'value': 'All'}]

for year in df['STARTDATE'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y').year).unique():
    year_options.append({'label': str(year), 'value': year})


print('years:',year_options)

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(id='yearPicker', options=year_options,
                     value='All', style={'width': '50%'}),
    ], style={'display': 'flex', 'justify-content': 'center', 'margin': '20px'}),

    dcc.Graph(
        id='firstGraph',
        config={'displayModeBar': False},
        style={'margin': '20px', 'marginLeft': '10%', 'width': '80%'}
    ),

    dcc.Graph(
        id='barGraph',
        config={'displayModeBar': False},
        style={'margin': '20px', 'marginLeft': '10%', 'width': '80%'}
    ),

    dcc.Graph(
        id='pieChart',
        config={'displayModeBar': False},
        style={'margin': '20px', 'marginLeft': '10%', 'width': '80%'}
    )
])


@app.callback(Output('firstGraph', 'figure'),
              Output('barGraph', 'figure'),
              Output('pieChart', 'figure'),
              [Input('yearPicker', 'value')])
def update_figure(selected_year):
    if selected_year == 'All':
        filtered_df = df

    else:
        filtered_df = df[df['STARTDATE'].apply(lambda x: datetime.strptime(x, '%d/%m/%Y').year) == selected_year]

    scatter_traces = []
    bar_data = []

    for device_name in filtered_df['MEDIATYPE'].unique():
        df_by_device = filtered_df[filtered_df['MEDIATYPE'] == device_name]
        print(df_by_device)
        scatter_traces.append(go.Scatter(
            x=df_by_device['STARTDATE'],
            y=df_by_device['MEDIATYPE'],
            mode='markers',
            opacity=0.7,
            marker={'size': 15},
            name=device_name
        ))

        bar_data.append({'x': [device_name], 'y': [len(df_by_device)], 'type': 'bar', 'name': device_name})

    scatter_layout = go.Layout(title='Scatter Plot', xaxis={'title': 'YEARS', 'automargin': True, 'title_standoff': 25},
                               yaxis={'title': 'DEVICES', 'automargin': True, 'title_standoff': 25})

    bar_layout = go.Layout(title='Bar Chart', xaxis={'title': 'DEVICES'}, yaxis={'title': 'COUNT'})

    # Create a pie chart using Plotly Express
    pie_chart = px.pie(filtered_df, names='MEDIATYPE', title='Pie Chart')

    return {'data': scatter_traces, 'layout': scatter_layout}, {'data': bar_data, 'layout': bar_layout}, pie_chart


if __name__ == '__main__':
    app.run_server()