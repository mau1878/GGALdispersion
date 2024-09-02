import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Fetch historical data for GGAL
ticker = "GGAL.BA"  # GGAL for Argentine stock market
start_date = st.date_input("Select the start date", value=pd.to_datetime('2020-01-01'))
end_date = st.date_input("Select the end date", value=pd.to_datetime('today'))

data = yf.download(ticker, start=start_date, end=end_date)

# Calculate 21-day SMA
data['21_SMA'] = data['Close'].rolling(window=21).mean()

# Calculate the dispersion (price - SMA)
data['Dispersion'] = data['Close'] - data['21_SMA']

# Plotly Line Plot: Historical Price with 21 SMA
fig = go.Figure()

# Plot the historical close price
fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close Price'))

# Plot the 21-day SMA
fig.add_trace(go.Scatter(x=data.index, y=data['21_SMA'], mode='lines', name='21 SMA'))

# Update layout
fig.update_layout(
    title=f"Historical Price of {ticker} with 21-day SMA",
    xaxis_title="Date",
    yaxis_title="Price (ARS)",
    legend_title="Legend",
    template="plotly_dark"
)

# Show the Plotly chart
st.plotly_chart(fig)

# Seaborn/Matplotlib Histogram: Dispersion with Percentiles
percentiles = [95, 75, 50, 25, 5]
percentile_values = np.percentile(data['Dispersion'].dropna(), percentiles)

plt.figure(figsize=(10, 6))
sns.histplot(data['Dispersion'].dropna(), kde=True, color='blue', bins=30)

# Add percentile lines
for percentile, value in zip(percentiles, percentile_values):
    plt.axvline(value, color='red', linestyle='--')
    plt.text(value, plt.ylim()[1]*0.9, f'{percentile}th', color='red')

plt.title(f'Dispersion of {ticker} Close Price from 21-day SMA')
plt.xlabel('Dispersion (ARS)')
plt.ylabel('Frequency')
st.pyplot(plt)
