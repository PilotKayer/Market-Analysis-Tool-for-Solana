"""
Designed by Davide Alejandro Castejon
All rights reserved

Name: Market Analysis Tool for Solana
Version: 0.0.1
"""
import pandas as pd
from src.market.market_service import MarketService
from src.market.activity_service import ActivityService
from src.types.activity import Activity
import datetime
from time import time

def set_up_dataframe(data):
    data = ActivityService.prepare_data(data)
    df = pd.DataFrame(data, columns=Activity.feature_names)
    print(df.head())

def test(name, days):
    x = MarketService()
    a = ActivityService()
    data = x.get_days_of_activities(name, days)
    return data
    # set_up_dataframe(data)


if __name__ == '__main__':
    # collection = input("Enter collection Name $>")
    # days = input("How many days worth of data? $>")
    # current = time()
    # to_remove = current - (2 * 24 * 60 * 60)
    # print(f'Now > {datetime.datetime.fromtimestamp(current)}')
    # print(f'Two days ago > {datetime.datetime.fromtimestamp(to_remove)}')
    data = test('elixir_ovols', 2)
    t = datetime.datetime.fromtimestamp(data[len(data)-1]['blockTime'])
    print(t)

