import pandas as pd

# URLs for the datasets
confirmed_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"

# Read the datasets
confirmed_df = pd.read_csv(confirmed_url)
deaths_df = pd.read_csv(deaths_url)
recovered_df = pd.read_csv(recovered_url)

# Save the preprocessed data for later use
confirmed_df.to_csv('confirmed_data.csv', index=False)
deaths_df.to_csv('deaths_data.csv', index=False)
recovered_df.to_csv('recovered_data.csv', index=False)
