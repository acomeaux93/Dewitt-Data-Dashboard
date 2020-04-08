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

#imports from MY program
import os
import dash_table
from six.moves.urllib.parse import quote

## Navbar
from navbar import Navbar

nav = Navbar()

# from jupyterlab_dash import AppViewer
# viewer = AppViewer()

#df = pd.read_csv('/Users/teacher/Desktop/DeWitt Data/1stsemestertotaldatafordataframe2.csv', dtype={"Student Name": object, "Off Class": object})

clinton_url='https://raw.githubusercontent.com/angelojc/dewittclinton/master/1stsemestertotaldatafordataframe2.csv'
df = pd.read_csv(clinton_url,sep=",")


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


pathway_list = ['Art','Engineering','Health','Macy','Other', "All Pathways"]
pathway_codes = ['A', 'E', 'H', 'M', 'G', "All"]

cohort_list = ['Y Cohort, class of 2023, 9th grade', 'X Cohort, class of 2022, 10th grade', 'W Cohort, class of 2021, 11th grade', 'V Cohort, class of 2020, 12th grade', 'U cohort, over age', 'All Cohorts']
cohort_codes = ['Y', 'X', 'W', 'V', 'U', "All"]

#App Layout
def AttendanceHeatMap():
    layout = html.Div([

        nav,

        html.Div([ html.Br()]),

         html.Div([
             html.H1(children='Student Attendance Data: Period Attendance Heat Map')
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
            html.Div([

                    html.H5(children='Select grade cohort and pathway'),

                    dcc.Dropdown(
                        id='cohort',
                        options=[{'label': cohort_list[i], 'value': i} for i in range(len(cohort_list))],
                        value= 5
                    ),
                    dcc.Dropdown(
                        id='pathway',
                        options=[{'label': pathway_list[i], 'value': i} for i in range(len(pathway_list))],
                        value= 5
                    )
            ],className="three columns"),

            html.Div([
               dcc.Graph(id='att_heatmap')
            ], className="three columns")

       ], className="row", style={'display':'block', 'margin-left':'auto', 'margin-right':'auto','width':'95%', 'border':'3px solid black', 'padding': '10px', 'backgroundColor': 'white'})

    ], style={'backgroundColor': 'whitesmoke'})

    return layout

def update_att_heat_graph(cohort,pathway):

    filter_df = df

    if cohort == 5:
        cohort_condition =filter_df['Student ID'].notnull()
    else:
        cohort_condition = filter_df['Off Class3']==cohort_codes[cohort]

    if pathway == 5:
        pathway_condition =filter_df['Student ID'].notnull()
    else:
        pathway_condition = filter_df['Off Class1']==pathway_codes[pathway]

    graph_me = df[cohort_condition & pathway_condition]

    graph_me = graph_me.sort_values(['Overall Rate']).reset_index(drop=True)

    attendance_rates = []

    for i in range(len(graph_me)):
        temp = []
        temp.append(graph_me['Percentage P1'][i])
        temp.append(graph_me['Percentage P2'][i])
        temp.append(graph_me['Percentage P3'][i])
        temp.append(graph_me['Percentage P4'][i])
        temp.append(graph_me['Percentage P5'][i])
        temp.append(graph_me['Percentage P6'][i])
        temp.append(graph_me['Percentage P7'][i])
        temp.append(graph_me['Percentage P8'][i])
        temp.append(graph_me['Percentage P9'][i])
        attendance_rates.append(temp)

    students = df['Student Name']

    figure = go.Figure(
        data= [
            go.Heatmap(
            x=['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5', 'Period 6', 'Period 7', 'Period 8', 'Period 9'],
            y=graph_me['Student Name'],
            #z=[graph_me['Percentage P1'], graph_me['Percentage P2'], graph_me['Percentage P3'], graph_me['Percentage P4'], graph_me['Percentage P5'], graph_me['Percentage P6'], graph_me['Percentage P7'], graph_me['Percentage P8'], graph_me['Percentage P9']],
            z=attendance_rates,
            colorscale=["red", "orange", "yellow", "green"],
            hoverongaps = False)
        ],
        layout=
            go.Layout(
            xaxis=dict(ticks=''),
            yaxis=dict(ticks=''),
            font=dict(size=10),
            plot_bgcolor='white',
            width=800,
            height=800,
            autosize=False
            )
    )

    figure.update_yaxes(showticklabels=False)


    return figure

    #viewer.show(app)
