import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Load preprocessed data
confirmed_df = pd.read_csv('confirmed_data.csv')
deaths_df = pd.read_csv('deaths_data.csv')
recovered_df = pd.read_csv('recovered_data.csv')

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Get the list of dates for the date range picker
dates = confirmed_df.columns[4:]

# Layout of the dashboard
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("COVID-19 Dashboard", className="text-center mb-4"), width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='country-dropdown',
                options=[{'label': country, 'value': country} for country in confirmed_df['Country/Region'].unique()],
                value='United States',
                className="mb-4"
            )
        ], width={"size": 6, "offset": 3})
    ]),
    dbc.Row([
        dbc.Col([
            dcc.DatePickerRange(
                id='date-picker-range',
                min_date_allowed=dates[0],
                max_date_allowed=dates[-1],
                start_date=dates[0],
                end_date=dates[-1],
                className="mb-4"
            )
        ], width={"size": 6, "offset": 3})
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='confirmed-trend'), width=12),
        dbc.Col(dcc.Graph(id='deaths-trend'), width=12),
        dbc.Col(dcc.Graph(id='recovered-trend'), width=12),
        dbc.Col(dcc.Graph(id='comparison-bar'), width=12),
        dbc.Col(dcc.Graph(id='map'), width=12)
    ])
], fluid=True)

# Function to plot trends
def plot_trends(df, country, metric, start_date, end_date):
    df_country = df[df['Country/Region'] == country].iloc[:, 4:].sum()
    df_country.index = pd.to_datetime(df_country.index)
    df_country = df_country[start_date:end_date]
    fig = px.line(df_country, title=f"{metric} Trend for {country}", labels={"index": "Date", "value": metric})
    fig.update_layout(template="plotly_dark", hovermode="x unified")
    fig.update_traces(hovertemplate='<b>Date</b>: %{x}<br><b>Value</b>: %{y}')
    return fig

def plot_comparison(df, date, metric):
    df_date = df.loc[:, ['Country/Region', date]].groupby('Country/Region').sum().reset_index()
    fig = px.bar(df_date, x='Country/Region', y=date, title=f"{metric} on {date}", labels={"Country/Region": "Country", date: metric})
    fig.update_layout(template="plotly_dark", hovermode="x unified")
    fig.update_traces(hovertemplate='<b>Country</b>: %{x}<br><b>Value</b>: %{y}')
    return fig

def plot_map(df, date, metric):
    df_date = df.loc[:, ['Country/Region', 'Lat', 'Long', date]].groupby(['Country/Region', 'Lat', 'Long']).sum().reset_index()
    fig = px.scatter_geo(df_date, lat='Lat', lon='Long', color=date, hover_name='Country/Region', size=date, title=f"Geographical Distribution of {metric} on {date}")
    fig.update_layout(template="plotly_dark")
    fig.update_traces(hovertemplate='<b>Country</b>: %{hovertext}<br><b>Value</b>: %{marker.size}')
    return fig


# Callbacks for interactivity
@app.callback(
    [Output('confirmed-trend', 'figure'),
     Output('deaths-trend', 'figure'),
     Output('recovered-trend', 'figure'),
     Output('comparison-bar', 'figure'),
     Output('map', 'figure')],
    [Input('country-dropdown', 'value'),
     Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date')]
)
def update_dashboard(country, start_date, end_date):
    date = confirmed_df.columns[-1]  # Latest date in the dataset
    return (
        plot_trends(confirmed_df, country, "Confirmed Cases", start_date, end_date),
        plot_trends(deaths_df, country, "Deaths", start_date, end_date),
        plot_trends(recovered_df, country, "Recovered", start_date, end_date),
        plot_comparison(confirmed_df, date, "Confirmed Cases"),
        plot_map(confirmed_df, date, "Confirmed Cases")
    )

dcc.DatePickerRange(
    id='date-picker-range',
    min_date_allowed=dates[0],
    max_date_allowed=dates[-1],
    start_date=dates[0],
    end_date=dates[-1],
    display_format='YYYY-MM-DD',
    start_date_placeholder_text='Start Date',
    end_date_placeholder_text='End Date',
    className="mb-4"
)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
