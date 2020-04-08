#THIS IS THE CREDIT ACCUMULATION PIE CHART

### Data
import pandas as pd
import pickle
### Graphing
import plotly.graph_objects as go

### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input

## Navbar
from navbar import Navbar

#imports from MY program
import os
import dash_table
from six.moves.urllib.parse import quote
from plotly.subplots import make_subplots

# from jupyterlab_dash import AppViewer
# viewer = AppViewer()

#Build App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#df = pd.read_csv('/Users/teacher/Desktop/DeWitt Data/creditsattemptedvsearnedpiechart.csv')

clinton_url='https://raw.githubusercontent.com/angelojc/dewittclinton/master/creditsattemptedvsearnedpiechart.csv'
df = pd.read_csv(clinton_url,sep=",")

df[' Count'] = range(1, len(df) + 1)

mid2020_differential = pd.Series(['float64'])
for i in range(len(df)):
    if df['Off Class 3'][i] == 'Y':
        mid2020_differential[i] = df['Earned'][i] - 5.5
    elif df['Off Class 3'][i] == 'X':
        mid2020_differential[i] = df['Earned'][i] - 16.5
    elif df['Off Class 3'][i] == 'W':
        mid2020_differential[i] = df['Earned'][i] - 27.5
    elif df['Off Class 3'][i] == 'V':
        mid2020_differential[i] = df['Earned'][i] - 33.5
    else:
        mid2020_differential[i] = df['Earned'][i] - 33.5

df.insert(15,"Mid2020 Differential", mid2020_differential)
df['Mid2020 Differential']=df['Mid2020 Differential'].astype(float)
df = df.round({'Mid2020 Differential': 3})


education_list = ['All Students','General Education', 'Special Education/504', 'ENL/ESL']
education_codes = [['1', '2', '3', '4', 'S', 'L', 'T', 'E', 'B',],['1', '2', '3', '4'],['S', 'L', 'T','E'],['B']]
#education_codes = [[1, 2, 3, 4],['S', 'L', 'T','E'],['B']]

nav = Navbar()

server = app.server

#App Layout
def CreditPieChart():
	layout = html.Div([

        nav,

        html.Div([ html.Br()]),

         html.Div([
             html.H1(children='Student Credit Data: On-track Credit Accumulation Breakdown')
        ], style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid crimson', 'padding': '10px', 'backgroundColor': 'white'}),

        html.Div([ html.Br()]),

         html.Div([
            html.H5(children='Description:'),

            dcc.Markdown('''
                * This dashboard shows the percentages and count of students in each cohort that are on or off track in terms of credit accumulation
                * The drop down menu can be used to look at subsets of student populations: General Education, Special Education, and ENL/ESL
                * Users can view the percentage and category totals by hovering over the graph sections
                * __This tool could be used to identify target students per cohort that are off track in terms of credit accumulation__
                '''),
        ],style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid black', 'padding': '10px', 'backgroundColor': 'white'}
        ),

        html.Div([ html.Br()]),

        html.Div([
            html.H5(children='Select student data set/subset'),

             dcc.Dropdown(
                 id='education',
                 options=[{'label': education_list[i], 'value': i} for i in range(len(education_list))],
                 value= 0
             ),

            dcc.Graph(id='pie')
        ], style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid black', 'padding': '10px', 'backgroundColor': 'white'}
        )
    ], style={'backgroundColor':'whitesmoke'})

	return layout

def update_credit_pie_graph(education):
    sub_df = df
    education_values = []
    education_items = education_codes[education]

    for item in education_items:
        education_values.append(item)

    print (education_values)

    education_conditions = df['Off Class 2'].isin(education_values)

    labels = ['On Track', 'Ahead of Track (5+ extra credits)', 'Off Track (0 - 5 credits behind)','Severely Off Track (more than 5 credits behind)']
    colors = ['green', 'blue', 'orange', 'red']

    fig = make_subplots(rows=1, cols=4, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])

    cohorts = ['Y', 'X', 'W', 'V']

    for i in range(len(cohorts)):
        filter_df = sub_df[education_conditions]
        cohort_df = filter_df[(filter_df['Off Class 3'] == cohorts[i])]

        categories = [0, 0 ,0, 0]

        categories[0] = len(cohort_df[(cohort_df['Mid2020 Differential'] >= 0) & (cohort_df['Mid2020 Differential'] <5)])
        categories[1] = len(cohort_df[(cohort_df['Mid2020 Differential'] >= 5)])
        categories[2] = len(cohort_df[(cohort_df['Mid2020 Differential'] < 0) & (cohort_df['Mid2020 Differential'] >-5)])
        categories[3] = len(cohort_df[(cohort_df['Mid2020 Differential'] < -5)])

        fig.add_trace(go.Pie(labels=labels, values=categories, name="testing"), 1, i + 1)

        fig.update_traces(hole=.4, marker=dict(colors=colors))

    fig.update_layout(
    title_text="Credit On-track percentage by cohort",
    # Add annotations in the center of the donut pies.
    annotations=[dict(text='Y cohort', x=0.08, y=0.5, font_size=12, showarrow=False),
                 dict(text='X cohort', x=0.37, y=0.5, font_size=12, showarrow=False),
                 dict(text='W cohort', x=0.63, y=0.5, font_size=12, showarrow=False),
                 dict(text='V cohort', x=0.92, y=0.5, font_size=12, showarrow=False)])

    return fig

    #viewer.show(app)
