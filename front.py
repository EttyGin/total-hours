import dash

# import dash_core_components as dcc
from dash import html, dcc

import plotly.graph_objects as go


app = dash.Dash(__name__)  # ), external_stylesheets=[dbc.themes.BOOTSTRAP])


def reset(total_dict: dict, spare_dict: dict) -> None:
    # יצירת הגרף
    fig_total = reset_graph(total_dict, "Attendance Summary")
    fig_spare = reset_graph(spare_dict, "Overtime Summary")

    fig_total.show()

    app.layout = html.Div(
        children=[
            html.H1(
                "--- OVERVIEW --",
                style={
                    "text-align": "center",
                    "font-family": "MV Boli",
                    "font-size": "18",
                    "color": "#636EFA",
                },
            ),
            dcc.Graph(
                id="total-graph",
                figure=fig_total,
            ),
            html.H3(
                f"Total {sum_work_hours(total_dict)}",
                style={
                    "text-align": "center",
                    "font-family": "MV Boli",
                    "color": "#00CC96",
                },
            ),
            dcc.Graph(
                id="spare-graph",
                figure=fig_spare,
            ),
            html.H3(
                f"Total {sum_work_hours(spare_dict)}",
                style={
                    "text-align": "center",
                    "font-family": "MV Boli",
                    "color": "#00CC96",
                },
            ),
        ]
    )


def reset_graph(data, title: str):
    dates = list(data.keys())
    hours = get_hours_in_str(data)

    colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A"]
    fig = go.Figure(
        data=[
            go.Bar(
                x=dates,
                y=hours,
                marker=dict(color=colors * len(dates)),  # חזרה על סדרת הצבעים
                text=list(data.values()),  # הוספת טקסט בתוך העמודות
                textposition="auto",
            )
        ]
    )

    # התאמות אישיות
    fig.update_layout(
        title={
            "text": title,
            "x": 0.5,  # מיקום אופקי במרכז (0-1)
            "y": 0.9,  # מיקום אנכי קרוב לחלק העליון (0-1)
            "xanchor": "center",  # יישור אופקי למרכז
            "yanchor": "top",  # יישור אנכי לחלק העליון
            "font": {
                "size": 24,  # גודל פונט
                "weight": "bold",  # גודל פונט
                "color": "#EF553B",  # צבע פונט
                "family": "MV Boli",  # משפחת פונט
            },
        },
        yaxis_title="Hours",
        yaxis_range=[min(hours), max(hours)],
        xaxis_tickvals=dates,
        xaxis_ticktext=dates,
        bargap=0.2,
    )

    return fig


def sum_work_hours(data) -> str:
    total_minutes = 0
    for time_str in data.values():
        hours, minutes = map(int, time_str.split(":"))
        total_minutes += hours * 60 + minutes

    total_hours = total_minutes // 60
    remaining_minutes = total_minutes % 60
    return f"{total_hours}:{remaining_minutes}"


def get_hours_in_str(total_dict):
    hours = []
    for hour_str in total_dict.values():
        # המרת שעה למספר עשרוני
        hour, minute = map(int, hour_str.split(":"))
        hours.append(hour + minute / 60)
    return hours
