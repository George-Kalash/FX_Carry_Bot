import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from MACD import compute_macd, should_buy, should_sell
from barAggregator import BarAggregator

CAN_SELL = False
CAN_BUY = True

buy_price = 0
total_return = 0

max_drawdown = 0

with open('historic_data.csv', 'r') as f:
    df = pd.read_csv(f)
  
barAggregator = BarAggregator(interval_seconds=300)

test_results = []


for index, row in df.iterrows():
  price = row['close']
  ts = pd.to_datetime(row['date']).timestamp() * 1000  # Convert to milliseconds
  barAggregator.update(price, int(ts))
  if len(barAggregator.bars) > 200:  # Ensure enough data for MACD calculation
    if CAN_BUY and should_buy(barAggregator.bars):
      test_results.append(f"BUY signal at {row['date']} with price {price}")
      CAN_BUY = False
      CAN_SELL = True
      buy_price = price
      print(f"BUY signal at {row['date']} with price {price}")
    elif CAN_SELL and should_sell(barAggregator.bars):
      test_results.append(f"SELL signal at {row['date']} with price {price}")
      CAN_SELL = False
      CAN_BUY = True
      total_return += (price - buy_price)
      max_drawdown = min(max_drawdown, price - buy_price)
      print(f"SELL signal at {row['date']} with price {price}, retutn: {(price - buy_price)}")

print(f"max_drawdown: {max_drawdown} \n total return: {total_return}")
with open('test_results', 'a') as f:
  for result in test_results:
    f.write(f"{result}\n")