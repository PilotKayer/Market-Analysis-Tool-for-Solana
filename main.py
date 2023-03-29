"""
Designed by Davide Alejandro Castejon
All rights reserved

Name: Market Analysis Tool for Solana
Version: 0.1.0
"""
import pandas as pd
from src.terminal.terminal import Terminal
from src.market.market_service import MarketService
from src.market.activity_service import ActivityService
from src.types.activity import Activity
from src.common.logger import Logger
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
    t = Terminal('0.1.0')
    t.start()

