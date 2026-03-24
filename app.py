import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px

df = pd.read_csv("data/output.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date").set_index("date")

# Aggregate to monthly total sales across all regions, drop last incomplete month
df_monthly = df["sales"].resample("ME").sum()
df_monthly = df_monthly[df_monthly.index < df_monthly.index[-1]].reset_index()

fig = px.line(
    df_monthly,
    x="date",
    y="sales",
    labels={"date": "Date", "sales": "Total Sales ($)"},
    title="Pink Morsel Sales Over Time (Monthly)",
    markers=True,
)

fig.add_vline(
    x=pd.Timestamp("2021-01-15").timestamp() * 1000,
    line_dash="dash",
    line_color="red",
    annotation_text="Price Increase",
    annotation_position="top left",
)

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualiser", style={"textAlign": "center"}),
    dcc.Graph(figure=fig),
])

if __name__ == "__main__":
    app.run(debug=True)
