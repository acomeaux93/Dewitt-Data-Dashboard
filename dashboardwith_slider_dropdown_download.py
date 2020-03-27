#I recommend installing the mini-condas package, comes with a ton of these modules
#Link here for Mac install https://conda.io/projects/conda/en/latest/user-guide/install/macos.html

# modules needed below plus install instruction links
# dash: https://anaconda.org/conda-forge/dash
# dash table: https://dash.plotly.com/datatable
# plotly: https://plotly.com/python/getting-started/
# pandas (look at miniconda installation): https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html
# Jupyter_lab and jupyter_dash: https://github.com/plotly/jupyterlab-dash

#imports
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

#Load and pre-process student data
url='https://raw.githubusercontent.com/angelojc/dewittclinton/master/creditsattemptedvsearnedSecret.csv'

df = pd.read_csv(url,sep=",")

accumulation_rate = pd.Series(['float64'])
for i in range(len(df)):
    if df["Attempted"][i] == 0:
        accumulation_rate[i] = 0.0
    else:
        accumulation_rate[i] = df["Earned"][i]/df["Attempted"][i]

df.insert(30,"Accumulation rate", accumulation_rate)
df['Accumulation rate']=df['Accumulation rate'].astype(float)

df = df.sort_values(['Attempted']).reset_index(drop=True)

grades =['9th Grade','10th Grade','11th Grade','12th Grade']
grade_frame = pd.DataFrame(grades)

percentages = [0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90, 0.95, 1.00]
percent_frame = pd.Series(percentages)


#Build Appviewer
#--> This is the extenstion that allows Dash apps to run in Jupyter Lab
#IMPORTANT: Jupyter lab is different that jupyter notebook. This will not run in notebook
# But if this a Heroku deployment, this should be commented out
# from jupyterlab_dash import AppViewer
# viewer = AppViewer()


#Build App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#Server connection below, should be uncommented in case of standalone deployment. Pairs with 'app.run_server' at bottom of page
server = app.server


#App Layout
app.layout = html.Div([
    html.Div([
            dcc.Dropdown(
                id='grade_level',
                options=[{'label': i, 'value': i} for i in ['9th Grade','10th Grade','11th Grade','12th Grade']],
                value= '9th Grade'
            )
    ]),

    html.Div([html.A(
        'Download Graph Data as .csv (this will change depending on filter settings)',
        id='download-link',
        download="rawdata.csv",
        href="",
        target="_blank"
        )
    ]),

    dcc.Graph(id='indicator-chart'),

        html.H3(children='Credit Attainment Percentage'),

    dcc.Slider(
        id='credit_percentage',
        min= 0.0,
        max= 1.0,
        value= 1.00,
        marks= {str(percent): str("{0:.0f}".format(percent * 100) + '%')  for percent in percent_frame},
        step= None
    ),

#     #Datatable hidden for now
#     dash_table.DataTable(
#     id='table',
#     columns=[{"name": i, "id": i} for i in df.columns],
#     style_cell={'textAlign': 'center'},
#     data=df.to_dict('records'),
#     )

])

# Callback for file download
@app.callback(
    Output('download-link', 'href'),
    [Input('grade_level', 'value'),
     Input('credit_percentage', 'value')]
)

# Defining the file download link
def update_download_link(gradelevel, slidervalue):
    filter_df = df[df['Accumulation rate'] <= slidervalue]

    is_freshman = filter_df['Level']==9
    freshman_df = filter_df[is_freshman]
    freshman_df = freshman_df.sort_values(['Earned']).reset_index(drop=True)

    is_sophomore = filter_df['Level']==10
    sophomore_df = filter_df[is_sophomore]
    sophomore_df = sophomore_df.sort_values(['Earned']).reset_index(drop=True)

    is_junior = filter_df['Level']==11
    junior_df = filter_df[is_junior]
    junior_df = junior_df.sort_values(['Earned']).reset_index(drop=True)

    is_senior = filter_df['Level']==12
    senior_df = filter_df[is_senior]
    senior_df = senior_df.sort_values(['Earned']).reset_index(drop=True)

    if gradelevel == '9th Grade':
        graph_me = freshman_df
    elif gradelevel == '10th Grade':
        graph_me = sophomore_df
    elif gradelevel == '11th Grade':
        graph_me = junior_df
    elif gradelevel == '12th Grade':
        graph_me = senior_df

    csv_string = graph_me.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8,%EF%BB%BF" + quote(csv_string)
    return csv_string


# Callback for Updating the figure
@app.callback(
    Output('indicator-chart', 'figure'),
    [Input('grade_level', 'value'),
     Input('credit_percentage', 'value')]
)

# Defining the Update Figure Here
def update_graph(gradelevel, slidervalue):

    filter_df = df[df['Accumulation rate'] <= slidervalue]

    is_freshman = filter_df['Level']==9
    freshman_df = filter_df[is_freshman]
    freshman_df = freshman_df.sort_values(['Earned']).reset_index(drop=True)

    is_sophomore = filter_df['Level']==10
    sophomore_df = filter_df[is_sophomore]
    sophomore_df = sophomore_df.sort_values(['Earned']).reset_index(drop=True)

    is_junior = filter_df['Level']==11
    junior_df = filter_df[is_junior]
    junior_df = junior_df.sort_values(['Earned']).reset_index(drop=True)

    is_senior = filter_df['Level']==12
    senior_df = filter_df[is_senior]
    senior_df = senior_df.sort_values(['Earned']).reset_index(drop=True)

    if gradelevel == '9th Grade':
        graph_me = freshman_df
    elif gradelevel == '10th Grade':
        graph_me = sophomore_df
    elif gradelevel == '11th Grade':
        graph_me = junior_df
    elif gradelevel == '12th Grade':
        graph_me = senior_df


# Return the Data Here
    return {
        'data': [
            {'x':graph_me.index, 'y':graph_me['Attempted'], 'type': 'bar', 'name': 'Attempted', 'text': "Student Name " + graph_me['FirstName'] +' '+ freshman_df['LastName'], 'hoverinfo': 'text'},
            {'x':graph_me.index, 'y':graph_me['Earned'], 'type': 'bar', 'name': 'Earned', 'text': "Student Name " + graph_me['FirstName'] +' '+ freshman_df['LastName'], 'hoverinfo': 'text'}
        ],
        'layout': {
            'title': 'Credits Attempted/Earned by Student',
            'xaxis': dict(title='Student'),
            'yaxis':dict(title='Credits'),
            'barmode':'overlay',
            'hovermode':'closest'
        }
    }


#Show app in Jupyter Lab
#This will be commented out if file is a Heroku deployment
#viewer.show(app)


#This section should be uncommented in case of standalone deployment. Pairs with 'server=app.server' higher up on page
if __name__ == '__main__':
    app.run_server(debug=True)
