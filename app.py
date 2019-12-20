#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#DAW Individual Project: Rossvern Reyes


# In[1]:


from IPython.display import display, IFrame, HTML
import os

def show_app(app, port=9999, width=900, height=700):
    host = 'localhost'
    url = f'http://{host}:{port}'

    display(HTML(f"<a href='{url}' target='_blank'>Open in new tab</a>"))
    display(IFrame(url, width=width, height=height))
    app.css.config.serve_locally = True
    app.scripts.config.serve_locally = True
    return app.run_server(debug=False, host=host, port=port)


# In[2]:


import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt

from dash.dependencies import Input, Output, State


# In[3]:


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


# In[4]:


app = dash.Dash(assets_folder='static/', external_stylesheets=external_stylesheets)


# In[6]:


df_atm = pd.read_csv('data/atm_data.csv')
df_bank = pd.read_csv('data/bank_data.csv')


# In[7]:


bank_3 = df_bank.groupby(['Region', 'Province', 'City/Municipality']).sum()


# In[8]:


df_1 = df_atm.groupby(['Region', 'Province', 'City/Municipality']).sum()


# In[9]:


app.callback_map = {}

app.layout = html.Div([
    html.Div([
        html.H3('A Visualization of the Physical Network of the Philippine Banking System',
               style={'color': '#0000A0'}),
        html.Label('Rossvern Reyes',
                  style={'font-style': 'italic'})
        ],
        style={
            'text-align': 'center'
        }),
    html.Br(),
    html.Div([
        html.P(
        "Part of the Philippine government’s thrust towards an inclusive economic growth is advancing " 
        "financial inclusion in the country. However, one of the hurdles in achieving an inclusive financial " 
        "system is the limited touchpoints to the banking system, particularly in the rural areas. " 
        "A survey of the central bank in 2018 revealed that only 22.6% of the adult Filipinos own a formal bank account. "
        "To gain a deeper understanding of the low level of participation in the formal banking system, this web "
        "application offers an interactive visualization of the distribution of bank offices and automated teller "
        "machines (ATMs) across the regions and provinces in the Philippines as of September 2019. "),
        html.Br(),
        html.P(
        "Source: Bangko Sentral ng Pilipinas (http://www.bsp.gov.ph/statistics/statnatmpbs.asp) "
                ),
    ],
            style={'width': '90%',
                   'display':'block',
                   'margin-left':'50px',
                   'margin-right':'10px',
                   'text-align':'justify'
              }),
    html.Hr(),
    html.Div([
        dcc.Dropdown(
            options=[{
                'label': i,
                'value': i} 
                for i in sorted(set(df_1.index.get_level_values(0)))
            ],
            placeholder='Step 1: Select Region',
            id='dd-region')
            ],
            style={
                     'width': '45%',
                     'display':'inline-block',
                     'margin-left':'50px',
                     'margin-right':'10px'
                  }
    ),
    html.Div([
        dcc.Dropdown(
            id='dd-province',
            placeholder='Step 2: Select Province')],
            style={
                    'width': '45%',
                    'display':'inline-block',
                    'margin-left':'5px'
              }
    ),
    html.Div([
        dcc.Graph(
            id='graph-regional-bank')],
            style={
                'width': '45%',
                'display':'inline-block',
                'margin':'10px'}
    ),
    html.Div([
        dcc.Graph(
            id='graph-bank')],
            style={
                'width': '45%',
                'display':'inline-block',
                'margin':'10px'}
    ),
    html.Div([
        dcc.Graph(
            id='graph-regional-atm')],
            style={
                'width': '45%',
                'display':'inline-block',
                'margin':'10px'}
    ),
    html.Div([
        dcc.Graph(
            id='graph-atm')],
            style={
                'width': '45%',
                'display':'inline-block',
                'margin':'10px'}
    ),
    html.Div([
    html.P(
        "An exploration of the plots above would show that over 85% of the cities and municipalities have zero to  "
        "very limited physical access to formal financing. Where Universal and Commercial Banks are not  "
        "available, Thrift Banks and Rural Banks are present, but only to a few areas. The presence of a banking  "
        "facility plays a vital role in an area’s growth and development, hence, the government’s agenda for  "
        "greater financial inclusion must overcome these physical barriers."
    )],
        style={
            'width': '90%',
            'display':'block',
            'margin-left':'50px',
            'margin-right':'10px',
            'text-align':'justify'
          }
    ),
])

#fill out provinces field
@app.callback(
    Output('dd-province', 'options'),
    [Input('dd-region', 'value')])

def update_prov(region):
    return [{
        'label': r,
        'value': r
    } for r in df_1.loc[df_1.index.get_level_values(0)==region].index.get_level_values(1).unique()]

#plot for no. of banks in selected region
@app.callback(
    Output('graph-regional-bank', 'figure'),
    [Input('dd-region', 'value')])

def regional_bank_graph(region):
    
    bank_2 = (df_bank.groupby(['Region', 'Province'])
                  ['Head Office', 
                   'Regular',
                   'Micro-finance Oriented', 
                   'Branch-lite Unit']
              .sum())
    
    bank_2 = bank_2.iloc[bank_2.index.get_level_values('Region') == region]
    
    trace1 = (go.Bar(
        x=bank_2.index.get_level_values(1), 
        y=bank_2['Head Office'], name='Head Office'))
    trace2 = (go.Bar(
        x=bank_2.index.get_level_values(1),
        y=bank_2['Regular'], name='Regular'))
    trace3 = (go.Bar(
        x=bank_2.index.get_level_values(1), 
        y=bank_2['Micro-finance Oriented'], name='Micro-finance Oriented'))
    trace4 = (go.Bar(
        x=bank_2.index.get_level_values(1), 
        y=bank_2['Branch-lite Unit'], name='Branch-lite Unit'))
    
    return {
        'data': [trace2, trace4, trace1, trace3], 
        'layout': {
        'title': f'Number of Bank Offices by Province',
        'xaxis': {
#             'title': 'Province',
            'categoryorder':'total descending',
#             'tickangle':'45'
            },
        'yaxis': {
            'title': 'Count',
            'categoryorder':'total descending'
            },
        'barmode':'stack',
        }
    }

#plot for no. of atms in selected region
@app.callback(
    Output('graph-regional-atm', 'figure'),
    [Input('dd-region', 'value')])

def regional_atm_graph(region):
    df_2 = (df_atm.groupby(
            ['Region', 'Province'])
            ['Rural', 'Thrift', 'UKB']
            .sum()
           )
    
    df_2 = df_2.iloc[df_2.index.get_level_values('Region') == region]
    
    trace1 = go.Bar(
        x=df_2.index.get_level_values(1), 
        y=df_2['Rural'], name='Rural Banks')
    trace2 = go.Bar(
        x=df_2.index.get_level_values(1), 
        y=df_2['Thrift'], name='Thrift Banks')
    trace3 = go.Bar(
        x=df_2.index.get_level_values(1), 
        y=df_2['UKB'], name='Universal and Commercial Banks')

    return {
        'data': [trace3, trace2, trace1], 
        'layout': {
        'title': f'Number of ATMs by Province',
        'xaxis': {
#             'title': 'Province',
            'categoryorder':'total descending',
#             'tickangle':'45'
            },
        'yaxis': {
            'title': 'Count',
            'categoryorder':'total descending'
            },
        'barmode':'stack',
        }
    }

#plot for no. of banks in selected province
@app.callback(
    Output('graph-bank', 'figure'),
    [Input('dd-region', 'value'),
    Input('dd-province', 'value')]
)

def provincial_bank_graph(region, province):
    bank_4 = (bank_3.iloc[(bank_3.index.get_level_values('Region') == region) & 
             (bank_3.index.get_level_values('Province') == province)])
    
    trace1 = (go.Bar(
                    x=bank_4.index.get_level_values(2), 
                    y=bank_4['Head Office'], 
                    name='Head Office'))
    trace2 = (go.Bar(
                    x=bank_4.index.get_level_values(2), 
                    y=bank_4['Regular'], 
                    name='Regular'))
    trace3 = (go.Bar(
                    x=bank_4.index.get_level_values(2), 
                    y=bank_4['Micro-finance Oriented'], 
                    name='Micro-finance Oriented'))
    trace4 = (go.Bar(
                    x=bank_4.index.get_level_values(2), 
                    y=bank_4['Branch-lite Unit'], 
                    name='Branch-lite Unit'))
    
    return {'data': [trace2, trace4, trace1, trace3], 
            'layout': {
            'title': f'Number of Bank Offices by City/Municipality',
            'xaxis': {
#                 'title': 'City/Municipality',
                'categoryorder':'total descending',
                'tickangle':'45'
                },
            'yaxis': {
                'title': 'Count',
                'categoryorder':'total descending'
                },
            'barmode':'stack',
            }}

#plot for no. of atms in selected province
@app.callback(
    Output('graph-atm', 'figure'),
    [Input('dd-region', 'value'),
    Input('dd-province', 'value')]
)

def provincial_atm_graph(region, province):
    df_3 = (df_1.iloc[(df_1.index.get_level_values('Region') == region) & 
                      (df_1.index.get_level_values('Province') == province)])
    
    trace1 = (go.Bar(
                    x=df_3.index.get_level_values(2), 
                    y=df_3['Rural'], 
                    name='Rural Banks'))
    trace2 = go.Bar(
                    x=df_3.index.get_level_values(2), 
                    y=df_3['Thrift'], 
                    name='Thrift Banks')
    trace3 = go.Bar(
                    x=df_3.index.get_level_values(2), 
                    y=df_3['UKB'], 
                    name='Universal and Commercial Banks')
    
    return {'data': [trace3, trace2, trace1], 
            'layout': {
                'title': f'Number of ATMs by City/Municipality',
                'xaxis': {
                    'categoryorder':'total descending',
                    'tickangle':'45'
                },
                'yaxis': {
                    'title': 'Count',
                    'categoryorder':'total descending'
                },
                'barmode':'stack'
            }
           }


# In[ ]:


if __name__ == '__main__':
    app.run_server(debug=True)


# In[11]:


show_app(app)


# In[ ]:




