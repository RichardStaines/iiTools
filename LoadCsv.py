import sys
import os

#from Model import db
#from Model.Dividend import *
from Model.db import *

import numpy as np
import pandas as pd
import timeit

sedol_map = {'B6T5S47': 'POLYMETAL',
             'BH0P3Z9': 'BHP',
             '216238': 'AV.',
             'B68SFJ1': 'Hend High Inc',
             'BDR8FC4': 'IND REIT'
             }
def load_csv(filename):
    df = pd.read_csv(filename, keep_default_na=True)

    print(df.columns)

    df['Description'] = df.apply(lambda row: 'Div' if 'Cash Distrib' in row.Description else row.Description,
        axis=1)

    df['Type'] = df.apply(
        lambda row: 'Interest' if row.Description.startswith('GROSS INTEREST') else 'Cash' if row.Description=='SUBSCRIPTION' or row.Description=='Carried forward cash balance' else 'Div' if row.Description.startswith('Div') else 'Trade',
        axis=1)

    # if ticker is missing replace with Sedol
    df['Symbol'] = df.apply(
        lambda row: sedol_map[row.Sedol] if str(row.Sedol) in sedol_map else row.Symbol, axis=1)

    df['Symbol'] = df.apply(
        lambda row: "SEDOL:" + str(row.Sedol) if str(row.Symbol) == 'nan' else row.Symbol, axis=1)

    df['Credit'] = df['Credit'].replace('[£,n/a]', '', regex=True).astype(float)
    df['Debit'] = df['Debit'].replace('[£,n/a]', '', regex=True).astype(float)
    df['Price'] = df['Price'].replace('[£,n/a]', '', regex=True).astype(float)

    # make the Qty negative for Sells
    df['BuySell'] = df.apply(
        lambda row: 'S' if row.Credit > 0 else r'B', axis=1)

    df['Consideration'] = df.apply(
        lambda row: row.Credit if row.Credit > 0 else row.Debit, axis=1)

    df['Datetime'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    print(df.info)

    divs = df.loc[df['Description'].str.startswith('Div')]
    print(f"Divs\n {divs.info}")

    interest = df.query('Type == "Interest"')
    print(f"Interest\n {interest.info}")

    trades = df.query('Type == "Trade"')
    print(f"\nTrades\n {trades.info}")

    cash = df.query('Type == "Cash"')
    print(f"\nCash\n {cash.info}")

    return interest, divs, trades, cash


def save_divs_from_df(divs):
    rec_list = [Dividend(instrument=div.Symbol,
                         sedol=div.Sedol,
                         description=div.Description,
                         amount=div.Credit,
                         trade_date=div.Datetime
                         ) for div in divs.itertuples()]
    print(rec_list)

    session.bulk_save_objects(rec_list)
    session.commit()


def save_cash_from_df(df):
    rec_list = [Cash(type=row.Type,
                     description=row.Description,
                     amount=row.Credit,
                     date=row.Datetime
                     ) for row in df.itertuples()]
    print(rec_list)
    session.bulk_save_objects(rec_list)
    session.commit()


def save_trades_from_df(df):
    rec_list = [Trade(instrument=trd.Symbol,
                      sedol=trd.Sedol,
                      instrument_description=trd.Description,
                      buy_sell=trd.BuySell,
                      quantity=trd.Quantity,
                      price=trd.Price,
                      net_consideration=trd.Consideration,
                      trade_date=trd.Datetime
                      ) for trd in df.itertuples()]
    print(rec_list)

    session.bulk_save_objects(rec_list)
    session.commit()



def main(argc, argv):
    app_name = os.path.basename(sys.argv[0])
    if argc < 2:
        print(f"Use: {app_name} <csvFile>")
        exit(1)

    filename = sys.argv[1]
    if os.path.isfile(filename) is False:
        print(f"File: {filename} does not exist")
        exit(1)

    print(f"{app_name} args {argc} Load file: {filename}")
    interest, divs, trades, cash = load_csv(filename)

    save_divs_from_df(divs)
    save_cash_from_df(cash)
    save_cash_from_df(interest)
    save_trades_from_df(trades)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
