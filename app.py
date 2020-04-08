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

## Navbar
from navbar import Navbar

nav = Navbar()

header = html.H3(
    'Testing Testing'
)

def App():
	layout = html.Div([
        nav,
        header
   	 ])
	return layout
