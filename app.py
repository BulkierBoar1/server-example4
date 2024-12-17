# Import packages
from dash import Dash, html, dash_table as dt, dcc, callback, Output, Input
import dash_ag_grid as dag
import pandas as pd
import plotly.express as px

# Use tabs to display specific brands and checkboxes to display specific products of the chosen brand on a grid.

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/Dash-Course/makeup-shades/shades.csv')

# Initialize the app
app = Dash(__name__)
server = app.sever

# Grid

grid = dag.AgGrid(
    id = 'Grid',
    rowData = [d for d in df.to_dict('records') if d['brand'] == 'Maybelline'],
    columnDefs = [{"field": i, 'sortable': False} for i in df.columns],
    columnSize = 'sizeToFit',
    dashGridOptions={"pagination": True, "animateRows": False},
)

# Tabs

tabs_styles = {
    'height': '44px', 'width': 'toFit'
}

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px'
}

# App layout
app.layout = html.Div([

    dcc.Tabs(id = "Brand Tabs", value = 'Maybelline', style = tabs_styles, 
            children = [dcc.Tab(label = tab, value = tab, 
                                style = tab_style, selected_style = tab_selected_style) 
                                for tab in set(df.get('brand'))]
            ),

    grid

])

# Add controls to build the interaction

@callback(
    Output(component_id = 'Grid',
           component_property = 'rowData'),

    Input(component_id = 'Brand Tabs',
          component_property = 'value')
)

def update_grid(brand):
    data = df.to_dict('records')
    data = [d for d in data if d['brand'] == brand]
    return data

# Run the app
if __name__ == '__main__':
    app.run(debug=True)