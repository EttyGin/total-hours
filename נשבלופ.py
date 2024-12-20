from datetime import datetime
import dash_bootstrap_components as dbc  # type: ignore
import dash

# import dash_core_components as dcc
from dash import html, dcc, Output, Input
import plotly.graph_objects as go


# Create a Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


def calculate_total_time(time_list):
    total_seconds = 0
    for time_str in time_list:
        # המרת מחרוזת ל-datetime.timedelta
        time_delta = datetime.strptime(time_str, "%H:%M:%S") - datetime(1900, 1, 1)
        total_seconds += time_delta.total_seconds()

    # חישוב שעות ודקות
    total_hours, remainder = divmod(total_seconds, 3600)
    total_minutes = remainder // 60

    return int(total_hours), int(total_minutes)


def reset(total_dict: dict) -> None:
    print(total_dict)
    # total_work_hours, total_work_minutes, total_spare_hours, total_spare_minutes

    # Create a bar chart
    fig = go.Figure(
        data=[go.Bar(x=[date], y=[hour]) for date, hour in total_dict.items()]
    )

    # Customize the chart
    fig.update_layout(
        title="Time in WORK!",
        xaxis_title="Day",
        yaxis_title="Total",
    )

    # Create the app layout
    app.layout = html.Div([dcc.Graph(id="my-graph", figure=fig)])
