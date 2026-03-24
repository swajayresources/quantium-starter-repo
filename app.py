import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

PRICE_INCREASE_DATE = pd.Timestamp("2021-01-15")

REGION_COLORS = {
    "north": "#FF6B6B",
    "east":  "#4ECDC4",
    "south": "#45B7D1",
    "west":  "#96CEB4",
    "all":   "#E84393",
}

app = dash.Dash(__name__)

app.layout = html.Div(
    style={
        "backgroundColor": "#1a1a2e",
        "minHeight": "100vh",
        "fontFamily": "'Segoe UI', sans-serif",
        "padding": "0 40px 40px",
    },
    children=[
        # Header
        html.Div(
            style={
                "textAlign": "center",
                "padding": "40px 0 20px",
                "borderBottom": "1px solid #16213e",
                "marginBottom": "30px",
            },
            children=[
                html.H1(
                    "Pink Morsel Sales Visualiser",
                    style={
                        "color": "#E84393",
                        "fontSize": "2.4rem",
                        "margin": "0 0 8px",
                        "letterSpacing": "1px",
                    },
                ),
                html.P(
                    "Soul Foods · Monthly Revenue by Region",
                    style={"color": "#8892b0", "fontSize": "1rem", "margin": 0},
                ),
            ],
        ),

        # Region filter
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "gap": "12px",
                "marginBottom": "24px",
            },
            children=[
                html.Span(
                    "Filter by region:",
                    style={"color": "#8892b0", "fontSize": "0.9rem"},
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": r.capitalize(), "value": r}
                        for r in ["all", "north", "east", "south", "west"]
                    ],
                    value="all",
                    inline=True,
                    inputStyle={"marginRight": "5px", "accentColor": "#E84393"},
                    labelStyle={
                        "color": "#ccd6f6",
                        "marginRight": "20px",
                        "fontSize": "0.95rem",
                        "cursor": "pointer",
                    },
                ),
            ],
        ),

        # Chart card
        html.Div(
            style={
                "backgroundColor": "#16213e",
                "borderRadius": "12px",
                "padding": "10px",
                "boxShadow": "0 4px 24px rgba(0,0,0,0.4)",
            },
            children=[dcc.Graph(id="sales-chart")],
        ),
    ],
)


@app.callback(Output("sales-chart", "figure"), Input("region-filter", "value"))
def update_chart(region):
    if region == "all":
        filtered = df
    else:
        filtered = df[df["region"] == region]

    monthly = (
        filtered.set_index("date")["sales"]
        .resample("ME")
        .sum()
    )
    # Drop last incomplete month
    monthly = monthly[monthly.index < monthly.index[-1]].reset_index()

    line_color = REGION_COLORS[region]

    fig = px.line(
        monthly,
        x="date",
        y="sales",
        labels={"date": "Date", "sales": "Total Sales ($)"},
        markers=True,
    )

    fig.update_traces(
        line={"color": line_color, "width": 2.5},
        marker={"color": line_color, "size": 6},
    )

    fig.add_vline(
        x=PRICE_INCREASE_DATE.timestamp() * 1000,
        line_dash="dash",
        line_color="#FF6B6B",
        line_width=1.5,
        annotation_text="Price Increase",
        annotation_font_color="#FF6B6B",
        annotation_position="top left",
    )

    region_label = "All Regions" if region == "all" else region.capitalize()

    fig.update_layout(
        title={
            "text": f"Monthly Sales — {region_label}",
            "font": {"color": "#ccd6f6", "size": 16},
            "x": 0.01,
            "xanchor": "left",
        },
        plot_bgcolor="#0f3460",
        paper_bgcolor="#16213e",
        font={"color": "#8892b0"},
        xaxis={
            "gridcolor": "#1a1a2e",
            "tickcolor": "#8892b0",
            "linecolor": "#8892b0",
            "title": {"text": "Date", "font": {"color": "#8892b0"}},
        },
        yaxis={
            "gridcolor": "#1a1a2e",
            "tickcolor": "#8892b0",
            "linecolor": "#8892b0",
            "title": {"text": "Total Sales ($)", "font": {"color": "#8892b0"}},
        },
        hovermode="x unified",
        hoverlabel={"bgcolor": "#1a1a2e", "font_color": "#ccd6f6"},
        margin={"t": 50, "b": 40, "l": 60, "r": 20},
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)
