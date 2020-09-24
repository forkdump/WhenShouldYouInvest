import yfinance as yf
from re import search
import numpy as np
from tqdm import tqdm
import random
import calendar
import pandas as pd
from lxml import html, etree
import requests
from datetime import date


def symbol_collector(input):
    if input[:4] == 'http':
        page = requests.get(input)
        tree = html.fromstring(page.content)
        table = tree.xpath('//table')
        symbols = pd.read_html(etree.tostring(table[0], method='html'))
        symbols = symbols[0]['Symbol'].to_list()
    else:
        symbols = pd.read_excel(input, header=None)[0].to_list()

    return symbols


def simulate_month_days_return(ticker_list, period, pickle_name='data_per_day'):
    database = pd.DataFrame(index=['Day ' + str(x) for x in range(1, 29)])
    raw_data = yf.download(ticker_list, period=period, group_by='ticker')
    filled_data = raw_data.fillna(method='ffill', limit=3).fillna(method='bfill', limit=3)
    tickers_data = filled_data.dropna(axis=1, how='any')

    ticker_list = tickers_data.columns.get_level_values(level=0).unique()

    for ticker in tqdm(ticker_list):
        ticker_data = tickers_data[ticker]
        ticker_data = ticker_data.resample('D', convention='end').asfreq().fillna(method='ffill')
        ticker_data['Returns'] = ticker_data['Adj Close'].pct_change() + 1

        day_returns = []
        trades = []
        total_values = []

        for day in range(1, 29):
            if day < 10:
                trade_moments = [i for i in ticker_data.index if search('....-..-0' + str(day), str(i))]
            else:
                trade_moments = [i for i in ticker_data.index if search('....-..-' + str(day), str(i))]

            ticker_data['Trades'] = 0

            total_value = []
            previous_row = 0

            for index, row in ticker_data.iterrows():
                if index in trade_moments:
                    previous_row = previous_row + 100

                total_value.append(previous_row * row['Returns'])

                if np.isnan(total_value[-1]):
                    previous_row = 0
                else:
                    previous_row = total_value[-1]

            day_returns.append(
                (total_value[-1] - len(trade_moments) * 100) / (len(trade_moments) * 100))
            total_values.append(total_value[-1])
            trades.append(len(trade_moments))

        database['Returns', ticker] = day_returns
        database['Total Value', ticker] = total_values
        database['Trade Moments', ticker] = trades

    database.columns = pd.MultiIndex.from_tuples(database.columns.to_list())

    database.to_pickle(pickle_name)

    return database


def simulate_random_days_return(ticker_list, period, simulations=2000, pickle_name='data_per_scenario'):
    def random_date(year, month):
        calendar_dates = calendar.Calendar()
        month_dates = calendar_dates.itermonthdates(year, month)

        return random.choice([date for date in month_dates if date.month == month])

    database = pd.DataFrame(index=['Simulation ' + str(x) for x in range(1, simulations + 1)])
    raw_data = yf.download(ticker_list, period=period, group_by='ticker')
    filled_data = raw_data.fillna(method='ffill', limit=3).fillna(method='bfill', limit=3)
    tickers_data = filled_data.dropna(axis=1, how='any')

    ticker_list = tickers_data.columns.get_level_values(level=0).unique()

    for ticker in ticker_list:
        ticker_data = tickers_data[ticker]
        ticker_data = ticker_data.resample('D').asfreq().fillna(method='ffill')
        ticker_data['Returns'] = ticker_data['Adj Close'].pct_change() + 1

        simulation_returns = []
        total_values = []
        trades = []
        dates_list = []

        for date_index in ticker_data.index:
            if (date_index.year, date_index.month) not in dates_list:
                dates_list.append((date_index.year, date_index.month))

        print("Performing simulation for " + ticker + "..")
        for simulation in tqdm(range(1, simulations + 1)):
            random_trade_dates = []
            for year_month in dates_list:
                month_date = random_date(year_month[0], year_month[1])

                if month_date > date.today():
                    random_trade_dates.append(date.today())
                else:
                    random_trade_dates.append(month_date)

            ticker_data['Trades'] = 0

            total_value = []
            previous_row = 0

            for index, row in ticker_data.iterrows():
                if index in random_trade_dates:
                    previous_row = previous_row + 100

                total_value.append(previous_row * row['Returns'])

                if np.isnan(total_value[-1]):
                    previous_row = 0
                else:
                    previous_row = total_value[-1]

            simulation_returns.append(
                (total_value[-1] - len(random_trade_dates) * 100) / (len(random_trade_dates) * 100))
            total_values.append(total_value[-1])
            trades.append(len(random_trade_dates))

        database['Returns', ticker] = simulation_returns
        database['Total Value', ticker] = total_values
        database['Trade Moments', ticker] = trades

    database.columns = pd.MultiIndex.from_tuples(database.columns.to_list())

    database.to_pickle(pickle_name)

    return database

