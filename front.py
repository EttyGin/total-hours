from datetime import datetime

import dash

# import dash_core_components as dcc
from dash import html, dcc, Output, Input

import plotly.graph_objects as go


app = dash.Dash(__name__)  # ), external_stylesheets=[dbc.themes.BOOTSTRAP])


def reset(total_dict: dict) -> None:
    # מיון המילון לפי מפתחות (תאריכים)
    sorted_dict = dict(sorted(total_dict.items()))

    # הכנת רשימות נפרדות לתאריכים ושעות
    dates = list(sorted_dict.keys())
    hours = []

    for hour_str in sorted_dict.values():
        # המרת שעה למספר עשרוני
        hour, minute = map(int, hour_str.split(":"))
        hours.append(hour + minute / 60)

        # הגדרת סדרת צבעים (ניתן לשנות)
    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]

    # יצירת הגרף
    fig = go.Figure(
        data=[
            go.Bar(
                x=dates,
                y=hours,
                marker=dict(color=colors * len(dates)),  # חזרה על סדרת הצבעים
                text=list(sorted_dict.values()),  # הוספת טקסט בתוך העמודות
                textposition="auto",
            )
        ]
    )

    # התאמות אישיות
    fig.update_layout(
        # title="Total hours per day:",
        xaxis_title="Date",
        yaxis_title="Hours",
        yaxis_range=[min(hours), max(hours)],
        xaxis_tickvals=dates,
        xaxis_ticktext=dates,
        # הוספת רווח בין העמודות
        bargap=0.2,
    )

    fig.show()

    # יצירת ממשק המשתמש
    app.layout = html.Div(
        children=[
            html.H1(
                "Total hours per day:",
                style={
                    "text-align": "center",
                    "font-family": "MV Boli",
                    "font-size": "18",
                    "color": "#636EFA",
                },
            ),
            dcc.Graph(
                id="my-graph",
                figure=fig,
            ),
        ]
    )
