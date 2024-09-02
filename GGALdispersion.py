import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Set the ticker to GGAL (ADR)
ticker = "GGAL"  # ADR for Grupo Financiero Galicia

# User input for date range
start_date = st.date_input("Select the start date", value=pd.to_datetime('2020-01-01'))
end_date = st.date_input("Select the end date", value=pd.to_datetime('today'))

# Fetch historical data for GGAL
data = yf.download(ticker, start=start_date, end=end_date)

# Calculate 21-day SMA
data['21_SMA'] = data['Close'].rolling(window=21).mean()

# Calculate the dispersion (price - SMA)
data['Dispersion'] = data['Close'] - data['21_SMA']

# Calculate the dispersion percentage
data['Dispersion_Percent'] = data['Dispersion'] / data['21_SMA'] * 100

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
    yaxis_title="Price (USD)",
    legend_title="Legend",
    template="plotly_dark"
)

# Show the Plotly chart
st.plotly_chart(fig)

# Plotly Line Plot: Historical Dispersion Percentage
fig_dispersion = go.Figure()

# Plot the dispersion percentage
fig_dispersion.add_trace(go.Scatter(x=data.index, y=data['Dispersion_Percent'], mode='lines', name='Dispersion %'))

# Update layout
fig_dispersion.update_layout(
    title=f"Historical Dispersion Percentage of {ticker}",
    xaxis_title="Date",
    yaxis_title="Dispersion (%)",
    legend_title="Legend",
    template="plotly_dark"
)

# Show the Plotly chart for dispersion percentage
st.plotly_chart(fig_dispersion)

# Seaborn/Matplotlib Histogram: Dispersion with Percentiles
percentiles = [95, 75, 50, 25, 5]
percentile_values = np.percentile(data['Dispersion'].dropna(), percentiles
