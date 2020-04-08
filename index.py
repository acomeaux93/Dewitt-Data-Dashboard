import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

#from credit_bargraph_app import CreditBarGraph #, build_graph
#from credit_piechart_app import CreditPieChart

import credit_bargraph_app
import credit_piechart_app
import period_attendance_heat_map_app
import regents_score_heatmap_app

from credit_bargraph_app import CreditBarGraph, update_credit_bar_graph, update_download_link
from credit_piechart_app import CreditPieChart, update_credit_pie_graph
from period_attendance_heat_map_app import AttendanceHeatMap, update_att_heat_graph
from regents_score_heatmap_app import RegentsScoreHeatMap, update_reg_score_graph

from homepage import Homepage

print(credit_bargraph_app.grades)

external_stylesheets = [dbc.themes.UNITED, 'https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = [dbc.themes.UNITED]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.config.suppress_callback_exceptions = True

server = app.server

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/credit-accumulation':
        print ("initiate accumulation")
        return credit_bargraph_app.CreditBarGraph()
    elif pathname == '/credit-track':
        return CreditPieChart()
    elif pathname =='/attendance-map':
        return AttendanceHeatMap()
    elif pathname =='/regents-map':
        return RegentsScoreHeatMap()
    else:
        return Homepage()


#Credit Bar chart callback: graph
@app.callback(
    [Output('indicator-chart', 'figure'),
     Output('chart-results', 'data')],
    [Input('grade_level', 'value'),
     Input('credit_percentage', 'value'),
     Input('my-id', 'value')]
)
def build_graph(gradelevel, slidervalue, password):
    graph = update_credit_bar_graph(gradelevel, slidervalue, password)
    return graph

#Credit Bar chart callback: download
@app.callback(
    Output('download-link', 'href'),
    [Input('grade_level', 'value'),
     Input('credit_percentage', 'value'),
     Input('my-id', 'value')]
)

def create_download(gradelevel, slidervalue, password):
    download = update_download_link(gradelevel, slidervalue, password)
    return download

#Pie chart callback: Graph
@app.callback(
    Output('pie', 'figure'),
    [Input('education', 'value')]
)

def update_pie(education):
    graph = update_credit_pie_graph(education)
    return graph

#Attendance Heat Map callback:
@app.callback(
    Output('att_heatmap', 'figure'),
    [Input('cohort', 'value'),
    Input('pathway', 'value')]
)

def update_att_heatmap(cohort, pathway):
    att_heatmap = update_att_heat_graph(cohort,pathway)
    return att_heatmap

#Regents Score Heat Map callbacks:
@app.callback(
    Output('reg_heatmap', 'figure'),
    [Input('exam', 'value'),
    Input('education', 'value'),
    Input('cohort', 'value'),
    Input('options', 'value')]
)

def update_reg_heatmap(exam, education, cohort, options):
    reg_heatmap = update_reg_score_graph(exam, education, cohort, options)
    return reg_heatmap


# @app.callback(
#     Output('output', 'children'),
#     [Input('pop_dropdown', 'value')]
# )
# def update_graph(city):
# 	graph = build_graph(city)
# 	return graph

if __name__ == '__main__':
    app.run_server(debug=True)
