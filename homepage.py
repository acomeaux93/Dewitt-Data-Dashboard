import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Welcome to SchoolDash!"),
            html.P( """Use the navigation bar up top to navigate between the data dashboard prototypes"""),

        ], md=4,),

        dbc.Col([
            html.Img(src="https://cdn4.creativecirclemedia.com/riverdalepress/original/1510780885_8c29.jpg", height="400px"),
            html.H3("Page Under Construction"),
        ]),
    ])
],className="mt-4",)

def Homepage():
	layout = html.Div([
	nav,
	body
	])

	return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = Homepage()

if __name__=="__main__":
	app.run_server()
