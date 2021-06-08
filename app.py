#!/usr/bin/env python

# Define default CJ color palette:
#palette = dict(blue="#007DC3", orange="#F8971D", red="#F31B23", lightblue="#ABD9E9")

import io
import base64
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import dash_table
import dash

import plotly.figure_factory as ff
import plotly.graph_objects as go

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def calculate_coverage(N, L, G):
    """Calculate read sequence coverage assuming uniform alignment.
    
    Where:
        N = number of reads
        L = approximate length of reads
        G = genome size (in base pairs)
    
    """
    return (N * L) / G

chips = {
    "Ion 510 Chip": [400, 200],
    "Ion 520 Chip": [600, 400, 200],
    "Ion 530 Chip": [600, 400, 200],
    "Ion 540 Chip": [200],
    "Ion 550 Chip": [200]
}

app.layout = html.Div([
    html.H6("Select the Ion Torrent chip:"),
    dcc.RadioItems(
        id = 'chip-selection-menu',
        options = [{"label": k, "value": k} for k in chips.keys()],
        value = "Ion 510 Chip"
    ),
    html.Hr(),
    html.H6("Select median read length:"),
    dcc.RadioItems(
        id = 'read-lengths-menu'
    ),
    html.Hr(),
    dcc.Input(
        id = 'genome-size-input',
        type = 'number',
        placeholder = "Input size in Mb"
    ),
    html.Hr(),
    dcc.Graph(
        id = 'calculate-sample-coverage'
    )
])

@app.callback(
     Output('read-lengths-menu', 'options'),
    [Input('chip-selection-menu', 'value')]
)
def update_read_lengths_dropdown(selected_chip):
    return [{"label": i, "value": i} for i in chips[selected_chip]]

@app.callback(
     Output('read-lengths-menu', 'value'),
    [Input('read-lengths-menu', 'options')]
)
def set_read_length(selected_length):
    return selected_length[0]['value']

@app.callback(
     Output('calculate-sample-coverage', 'figure'),
    [Input('chip-selection-menu', 'value'),
     Input('read-lengths-menu', 'value'),
     Input('genome-size-input', 'value')]
)
def display_sample_coverage(selected_chip, selected_length, genome_size):
    # Import Ion Torrent chip specifications:
    df = pd.read_csv('data/torrent.txt')
    
    n_reads = (
        df.reads[(df.chip == selected_chip) & (df.length == selected_length)].to_numpy()[0])
    
    coverage = (n_reads * selected_length) / (genome_size * 1e6)

    return {
        "data": [dict(
            x = [i for i in np.arange(1,25)],
            y = [(coverage/N) for N in np.arange(1,25)],
            mode = "markers+lines",
            marker = {
                "size": 15,
                "opacity": 0.5,
                "line": {"width": 0.5, "color": "black"}
            }
        )],
        "layout": dict(
            xaxis = {
                "title": "Number of Samples"
            },
            yaxis = {
                "title": "Coverage"
            },
            height = 500,
            hovertext = [f"{coverage/N}X" for N in np.arange(1,25)],
            hovermode = "closest",
            hoverformat = ".1f"
        )
    }

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8051, debug=False, dev_tools_ui=False,dev_tools_props_check=False)
    #app.run_server(host='0.0.0.0', port=8051, debug=True)
