import yfinance as yf
import yahooquery as yq
import pandas as pd
import asyncio

tickers = yq.Ticker('meta')

df = tickers.history(period='max', interval='1d')

df.head()

print(df)