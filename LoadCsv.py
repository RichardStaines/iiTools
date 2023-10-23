import sys
import os

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
    df['type'] = df.apply(
        lambda row: 'Interest' if row.Description.startswith('GROSS INTEREST') else 'Cash' if row.Description=='SUBSCRIPTION' or row.Description=='Carried forward cash balance' else 'Div' if row.Description.startswith('Div') else 'Trade',
        axis=1)

    # if ticker is missing replace with Sedol
    df['Symbol'] = df.apply(
        lambda row: sedol_map[row.Sedol] if str(row.Sedol) in sedol_map else row.Symbol, axis=1)

    df['Symbol'] = df.apply(
        lambda row: "SEDOL:" + str(row.Sedol) if str(row.Symbol) == 'nan' else row.Symbol, axis=1)

    df['Credit'] = df['Credit'].replace('[£,n/a]', '', regex=True).astype(float)
    df['Debit'] = df['Debit'].replace('[£,n/a]', '', regex=True).astype(float)

    # make the Qty negative for Sells
    df['Quantity'] = df.apply(
        lambda row: -row.Quantity if row.Credit > 0 else row.Quantity, axis=1)

    df['Datetime'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    print(df.info)

    divs = df.loc[df['Description'].str.startswith('Div')]
    print(f"Divs\n {divs.info}")

    interest = df.query('type == "Interest"')
    print(f"Interest\n {interest.info}")

    trades = df.query('type == "Trade"')
    print(f"\nTrades\n {trades.info}")

    cash = df.query('type == "Cash"')
    print(f"\nCash\n {cash.info}")

    return interest, divs, trades, cash


def sum_by_year(df, title=None):
    # totals = df.groupby(df['Datetime'].dt.year).agg({'Debit' : 'sum', 'Credit': 'sum'})
    totals = df.groupby(df['Datetime'].dt.year).agg(Buy_Debit=('Debit' , 'sum'), Sell_Credit=('Credit', 'sum') )
    if title is not None:
        print (f"\n\n{title}:")
    print(totals)

def sum_by_symbol_and_year(df, title=None, include_qty=False):
    if include_qty:
        totals = df.groupby(['Symbol', df['Datetime'].dt.year] ).agg(Qty=('Quantity', 'sum'), Buy_debit=('Debit', 'sum'), Sell_credit=('Credit', 'sum'))
    else:
        totals = df.groupby(['Symbol', df['Datetime'].dt.year] ).agg(Buy_debit=('Debit', 'sum'), Sell_credit=('Credit', 'sum'))
    if title is not None:
        print (f"\n\n{title}:")
    print(totals)

def sum_by_symbol(df, title=None, include_qty=False):
    if include_qty:
        totals = df.groupby('Symbol').agg(Qty=('Quantity', 'sum'), Buy_Debit=('Debit', 'sum'), Sell_Credit=('Credit', 'sum'))
    else:
        # totals = df.groupby('Symbol').agg({'Debit' : 'sum', 'Credit': 'sum'})
        totals = df.groupby('Symbol').agg(Buy_Debit=('Debit', 'sum'), Sell_Credit=('Credit', 'sum'))

    if title is not None:
        print (f"\n\n{title}:")
    print(totals)

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

    # my divs each year...
    sum_by_year(interest, "Interest")

    sum_by_year(divs, "Divs by Year")
    sum_by_symbol_and_year(divs, "Divs by Symbol and Year")
    sum_by_symbol(divs, 'Divs by Symbol')

    sum_by_year(cash, "Cash")

    # my trading activity
    # The Qty doesnt always make sense as the csv file has no starting positions and nothing before 2021
    sum_by_symbol(trades, "Trades by Symbol", include_qty=True)
    sum_by_symbol_and_year(trades, "Trades by Symbol and Year", include_qty=True)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
