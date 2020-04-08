#THIS IS THE CREDIT ACCUMULATION BAR GRAPH

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

# header = html.H3(
#     'Testing Testing Credit Bar Graph'
# )
#
# def CreditBarGraph():
# 	layout = html.Div([
#         nav,
#         header
#    	 ])
# 	return layout

def CreditBarGraph():
#Load and pre-process anonymous student data
    safe_url='https://raw.githubusercontent.com/angelojc/dewittclinton/master/creditsattemptedvsearnedSecret.csv'

    df = pd.read_csv(safe_url,sep=",")

    df[' Count'] = range(1, len(df) + 1)

    accumulation_rate = pd.Series(['float64'])
    for i in range(len(df)):
        if df["Attempted"][i] == 0:
            accumulation_rate[i] = 0.0
        else:
            accumulation_rate[i] = df["Earned"][i]/df["Attempted"][i]

    df.insert(30,"Accumulation rate", accumulation_rate)
    df['Accumulation rate']=df['Accumulation rate'].astype(float)
    df = df.round({'Accumulation rate': 3})

    df = df.sort_values(['Attempted']).reset_index(drop=True)


    #Load and pre-process clinton student data
    clinton_url='https://raw.githubusercontent.com/angelojc/dewittclinton/master/creditsattemptedvsearned.csv'

    clinton_df = pd.read_csv(clinton_url,sep=",")

    clinton_df[' Count'] = range(1, len(df) + 1)

    accumulation_rate = pd.Series(['float64'])
    for i in range(len(clinton_df)):
        if clinton_df["Attempted"][i] == 0:
            accumulation_rate[i] = 0.0
        else:
            accumulation_rate[i] = clinton_df["Earned"][i]/clinton_df["Attempted"][i]

    clinton_df.insert(30,"Accumulation rate", accumulation_rate)
    clinton_df['Accumulation rate']=clinton_df['Accumulation rate'].astype(float)
    clinton_df = clinton_df.round({'Accumulation rate': 3})

    clinton_df = clinton_df.sort_values(['Attempted']).reset_index(drop=True)

    #Pre-processing data structures for graph
    grades =['9th Grade','10th Grade','11th Grade','12th Grade']
    grade_frame = pd.DataFrame(grades)

    percentages = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
    percent_frame = pd.Series(percentages)


    #Build Appviewer
    #--> This is the extenstion that allows Dash apps to run in Jupyter Lab
    #IMPORTANT: Jupyter lab is different that jupyter notebook. This will not run in notebook
    # from jupyterlab_dash import AppViewer
    # viewer = AppViewer()


    #Build App
    external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    #Server connection below, should be uncommented in case of standalone deployment on Heroku. Pairs with 'app.run_server' at bottom of page
    #server = app.server

    #App Layout
    app.layout = html.Div([

        #navbar
        nav,

        #Ghetto password input field.

        html.Div([ html.P('Please enter password to view dashboard with student data'),
                  dcc.Input(id='my-id', value='', type='text'),
                  html.Br()]),

        html.Div([ html.Br()]),

        html.H5(children='Description:'),

        dcc.Markdown('''
            * This program shows a dynamic graph of students and their school credit history. It displays an overlay bar graph of credits earned on top of credits attempted
            * The graph and table changes based on two input variables, the "Grade Level" drop down menu and "Credit accumulation percentage" slider
            * Users can view the names of students by hovering over the graph values
            * Users can click the download link to download a .csv file of table values for their custom graph
            * This tool could be used to identify target students per grade level that have a history of low credit attainment
            '''),

        html.Div([ html.Br()]),

        html.P('Student data is initially anonymous. To interact with real Clinton data, enter the correct password into the input field at the top of the page'),

        html.Div([ html.Br()]),

        html.H5(children='Select Grade Level to View'),

        html.Div([
                dcc.Dropdown(
                    id='grade_level',
                    options=[{'label': i, 'value': i} for i in ['9th Grade','10th Grade','11th Grade','12th Grade','All Grades']],
                    value= 'All Grades'
                )
        ]),



        dcc.Graph(id='indicator-chart'),

        html.H5(children='Select Credit Attainment Percentage Range to View'),

        dcc.Slider(
            id='credit_percentage',
            min= 0.0,
            max= 1.0,
            value= 1.00,
            marks= {str(percent): str("{0:.0f}".format(percent * 100) + '%')  for percent in percent_frame},
            step= None
        ),

        html.Div([ html.Br(),html.Br()]),

        html.Div([html.A(
            'Download Graph Data as .csv',
            id='download-link',
            download="rawdata.csv",
            href="",
            target="_blank"
            ),
            html.P('Clicking this link will download a .csv file with table data of the current set graph. Data will contain information presented below plus extra columns')
        ]),

        html.Div([ html.Br()]),

        html.Div([
            dash_table.DataTable(
                id='chart-results',
                columns=[{"name": i, "id": i} for i in df.loc[:,[' Count','StudentID','LastName','FirstName','OffClass','Grade','Level','Attempted','Earned','Accumulation rate']]],
                style_cell={'textAlign': 'center'},
            )
            ]
        )


    ])

    # Callback for file download
    @app.callback(
        Output('download-link', 'href'),
        [Input('grade_level', 'value'),
         Input('credit_percentage', 'value'),
         Input('my-id', 'value')]
    )

    # Defining the file download link
    # Has case for determining if password is set correctly, will show Clinton data if password is correct
    def update_download_link(gradelevel, slidervalue, password):

        if password == 'clintonhs':
            filter_df = clinton_df[clinton_df['Accumulation rate'] <= slidervalue]
        else:
            filter_df = df[df['Accumulation rate'] <= slidervalue]

        filter_df = filter_df.sort_values(['Attempted']).reset_index(drop=True)

        is_freshman = filter_df['Level']==9
        freshman_df = filter_df[is_freshman]
        freshman_df = freshman_df.sort_values(['Attempted']).reset_index(drop=True)

        is_sophomore = filter_df['Level']==10
        sophomore_df = filter_df[is_sophomore]
        sophomore_df = sophomore_df.sort_values(['Attempted']).reset_index(drop=True)

        is_junior = filter_df['Level']==11
        junior_df = filter_df[is_junior]
        junior_df = junior_df.sort_values(['Attempted']).reset_index(drop=True)

        is_senior = filter_df['Level']==12
        senior_df = filter_df[is_senior]
        senior_df = senior_df.sort_values(['Attempted']).reset_index(drop=True)

        if gradelevel == '9th Grade':
            graph_me = freshman_df
        elif gradelevel == '10th Grade':
            graph_me = sophomore_df
        elif gradelevel == '11th Grade':
            graph_me = junior_df
        elif gradelevel == '12th Grade':
            graph_me = senior_df
        elif gradelevel == 'All Grades':
            graph_me = filter_df

        csv_string = graph_me.to_csv(index=False, encoding='utf-8')
        csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
        return csv_string


    # Callback for Updating the figure
    @app.callback(
        [Output('indicator-chart', 'figure'),
         Output('chart-results', 'data')],
        [Input('grade_level', 'value'),
         Input('credit_percentage', 'value'),
         Input('my-id', 'value')]
    )

    # Defining the Update Figure and Table Here
    # Has case for determining if password is set correctly, will show Clinton data if password is correct
    def update_graph(gradelevel, slidervalue, password):

        if password == 'clintonhs':
            filter_df = clinton_df[clinton_df['Accumulation rate'] <= slidervalue]
        else:
            filter_df = df[df['Accumulation rate'] <= slidervalue]

        filter_df = filter_df.sort_values(['Attempted']).reset_index(drop=True)

        is_freshman = filter_df['Level']==9
        freshman_df = filter_df[is_freshman]
        freshman_df = freshman_df.sort_values(['Attempted']).reset_index(drop=True)

        is_sophomore = filter_df['Level']==10
        sophomore_df = filter_df[is_sophomore]
        sophomore_df = sophomore_df.sort_values(['Attempted']).reset_index(drop=True)

        is_junior = filter_df['Level']==11
        junior_df = filter_df[is_junior]
        junior_df = junior_df.sort_values(['Attempted']).reset_index(drop=True)

        is_senior = filter_df['Level']==12
        senior_df = filter_df[is_senior]
        senior_df = senior_df.sort_values(['Attempted']).reset_index(drop=True)

        if gradelevel == '9th Grade':
            graph_me = freshman_df
        elif gradelevel == '10th Grade':
            graph_me = sophomore_df
        elif gradelevel == '11th Grade':
            graph_me = junior_df
        elif gradelevel == '12th Grade':
            graph_me = senior_df
        elif gradelevel == 'All Grades':
            graph_me = filter_df

        graph_me[' Count'] = range(1, len(graph_me) + 1)


    # Create graph
        figure = go.Figure(
            data=[
                go.Bar(name="Credits Attempted", x=graph_me.index, y=graph_me['Attempted'],marker_color= "black",text="Student Name " + graph_me['FirstName'] +' '+ graph_me['LastName'], hoverinfo='text'),
                go.Bar(name="Credits Earned", x=graph_me.index, y=graph_me['Earned'],text="Student Name " + graph_me['FirstName'] +' '+ graph_me['LastName'], hoverinfo='text')
            ],
            layout=go.Layout(title='Credits Attempted vs. Earned by Student',xaxis=dict(title='Students'),yaxis=dict(title='Credits Attempted'),barmode='overlay',hovermode='closest', plot_bgcolor='whitesmoke')
        )

        figure.update_xaxes(showticklabels=False)

        # Update Table
        data=graph_me.to_dict('records')

        return figure, data

    # Return the Data Here
    # This was for the old graph object notation. This could only return one item, the graph object. I changed notations to the one above
    # because I needed to return two variables so I wrapped up the graph into a figure object

    #     return {
    #         'data': [
    #             {'x':graph_me.index, 'y':graph_me['Attempted'], 'type': 'bar', 'name': 'Attempted', 'text': "Student Name " + graph_me['FirstName'] +' '+ graph_me['LastName'], 'hoverinfo': 'text'},
    #             {'x':graph_me.index, 'y':graph_me['Earned'], 'type': 'bar', 'name': 'Earned', 'text': "Student Name " + graph_me['FirstName'] +' '+ graph_me['LastName'], 'hoverinfo': 'text'}
    #         ],
    #         'layout': {
    #             'title': 'Credits Attempted/Earned by Student',
    #             'xaxis': dict(title='Student'),
    #             'yaxis':dict(title='Credits'),
    #             'barmode':'overlay',
    #             'hovermode':'closest'
    #         }
    #     }

    #Show app in Jupyter Lab
    # viewer.show(app)


    #This section should be uncommented in case of standalone deployment. Pairs with 'server=app.server' higher up on page
    if __name__ == '__main__':
        app.run_server(debug=True)

    return app.layout
