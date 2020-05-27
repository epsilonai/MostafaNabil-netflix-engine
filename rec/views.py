import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from rec import recommendations ,generate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

dash_app = dash.Dash(__name__,external_stylesheets=external_stylesheets)

server = dash_app.server

dash_app.layout = html.Div([
    html.H1("Recommendation Engine", style={"text-align":"center"}),

    html.Div(
        [
            dcc.Input(placeholder="Enter Here ...",
                      id="Title",
                      style={"width":"60%"},
                    ),
            
            html.Button(id='submit-button',
                        n_clicks=0,
                        children="Submit"),
            
            html.Div(id='dummy')
        ],

        style={ "text-align" : "center" ,
                "width" : "100%" ,
                "columcount":2}
    ),
    
    html.H4("Must Watch :",style={"text-align":"center"}),

        html.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Recommended"),
                            
                        ]
                    )
                ),
                html.Tbody(
                    [
                        html.Th("1-"),
                        html.Th("2-"),
                        html.Th("3-"),
                        html.Th("4-"),
                        html.Th("5-"),
                    ],
                    id="rec-table"
                )
            ], style={"width": "100%"}
        ),
    html.H4("Random Titles :",style={"text-align":"center"}),

    html.Table([
        html.Thead(
            html.Tr([
                html.Th("Choose one of these titles")
            ])
        ),
        html.Tbody(
            [
                html.Th("1-"),
                html.Th("2-"),
                html.Th("3-"),
                html.Th("4-"),
                html.Th("5-"),
            ],
            id="random"
        )
    ],style={"width": "100%"}
    ),

])

# ------------------------------- CALLBACKS ---------------------------------------- #

@dash_app.callback(Output("dummy", "children"),
                   [Input("submit-button", "n_clicks")],
                   [State("Title", "value")])

def new_search(n_clicks, Title):
    if not Title:
        return "Please enter Title"
    print(f"got a Title:{Title}")
    recommendations(Title)
    return f"Trying to find a match for {Title}" 


@dash_app.callback(Output("rec-table" , "children"),
                    [Input("submit-button" , "n_clicks")],
                    [State("Title", "value")])

def update(n_clicks , Title):
    similar = recommendations(Title)
    return [
        html.Th(similar[0]),
        html.Th(similar[1]),
        html.Th(similar[2]),
        html.Th(similar[3]),
        html.Th(similar[4]),
    ]

@dash_app.callback(Output("random" , "children"),
                   [Input("submit-button","n_clicks")])
            
def update_1(n_clicks):
    random_1=generate()
    return [
        html.Th(random_1[0]),
        html.Th(random_1[1]),
        html.Th(random_1[2]),
        html.Th(random_1[3]),
        html.Th(random_1[4]),
    ]