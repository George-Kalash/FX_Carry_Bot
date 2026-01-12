# Readme

## Requirements

- Python 3.x
- yfinance
- asyncio

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```


example of a live stream: 
```python
import asyncio
import yfinance as yf

latest = {}
last_seen = {}
def on_message(msg):
  symbol = msg["id"]
  price = msg["price"]
  ts = msg["time"]

  prev = last_seen.get(symbol)

  if prev is None or prev["price"] != price or prev["time"] != ts:
    last_seen[symbol] = msg
    print(last_seen[symbol])

async def live_data_stream(ticker_symbol, callback):
  async with yf.AsyncWebSocket() as ws:
    await ws.subscribe([ticker_symbol])
    await ws.listen(callback)

async def main():
  ticker_symbol = "BYND"
    
  stream_task = asyncio.create_task(live_data_stream(ticker_symbol, on_message))

  try:
    while True:
      if ticker_symbol in latest:
        
        print(f"Latest data for {ticker_symbol}: {latest[ticker_symbol]}")
      await asyncio.sleep(1)
  finally:
    stream_task.cancel()
```