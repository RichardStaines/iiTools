import sys
import os
import pandas as pd
import timeit


def load_csv(filename):
    df = pd.read_csv(filename)

    print(df.columns)
    df['type'] = df.apply(
        lambda row: 'Interest' if row.Description == 'GROSS INTEREST' else 'Cash' if row.Description=='SUBSCRIPTION' else 'Div' if row.Description.startswith('Div') else 'Trade',
        axis=1)

    df['Credit'] = df['Credit'].replace('[£,n//a]', '', regex=True).astype(float)
    df['Debit'] = df['Debit'].replace('[£,n//a]', '', regex=True).astype(float)

    df['Datetime'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    print(df.info)

    divs = df.loc[df['Description'].str.startswith('Div')]
    print(f"Divs\n {divs.info}")

    interest = df.query('type == "Interest"')
    print(f"Trades\n {interest.info}")

    trades = df.query('type == "Trade"')
    print(f"\nTrades\n {trades.info}")

    cash = df.query('type == "Cash"')
    print(f"\nCash\n {cash.info}")

    return interest, divs, trades, cash


def sum_by_year(df, title=None):
    totals = df.groupby(df['Datetime'].dt.year).agg({'Debit' : 'sum', 'Credit': 'sum'})
    if title is not None:
        print (f"\n\n{title}:")
    print(totals)


def main(argc, argv):
    app_name = os.path.basename(sys.argv[0])
    if argc < 2:
        print(f"Use: {app_name} <csvFile>")
        exit(1)

    filename = sys.argv[1]
    print(f"{app_name} args {argc} Load file: {filename}")
    _, divs, trades, cash = load_csv(filename)

    # my divs each year...
    sum_by_year(divs, "Divs")

    sum_by_year(cash, "Cash")

    # my trading activity

    # sum_by_year(trades, "Trades")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
