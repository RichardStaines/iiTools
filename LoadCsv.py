import sys
import os
import argparse
import pandas as pd

from Utils.iiCSV import IICsv
from Model.db import *


def save_divs_from_df(divs, portfolio):

    rec_list = [Dividend(instrument=div.Symbol,
                         sedol=div.Sedol,
                         description=div.Description,
                         amount=div.Credit,
                         payment_date=div.Datetime,
                         portfolio=portfolio
                         ) for div in divs.itertuples()]
    print(rec_list)

    session.bulk_save_objects(rec_list)
    session.commit()


def save_cash_from_df(df, portfolio):
    rec_list = [Cash(type=row.Type,
                     description=row.Description,
                     amount=row.Credit,
                     payment_date=row.Datetime,
                     portfolio=portfolio
                     ) for row in df.itertuples()]
    print(rec_list)
    session.bulk_save_objects(rec_list)
    session.commit()


def save_trades_from_df(df, portfolio):
    rec_list = [Trade(instrument=trd.Symbol,
                      sedol=trd.Sedol,
                      instrument_description=trd.Description,
                      buy_sell=trd.BuySell,
                      quantity=trd.Quantity,
                      price=trd.Price,
                      net_consideration=trd.Consideration,
                      trade_date=trd.Datetime,
                      portfolio=portfolio
                      ) for trd in df.itertuples()]
    print(rec_list)

    session.bulk_save_objects(rec_list)
    session.commit()


def process_commandline():
    parser = argparse.ArgumentParser(
        usage="%(prog)s -p <portfolio> <II-csv-filename>"
    )
    parser.add_argument(
        "-p", "--portfolio", default=''
    )
    parser.add_argument("filename")  # positional parameter so mandatory
    args = parser.parse_args()
    # print(args)
    return args


def main(argc, argv):
    app_name = os.path.basename(sys.argv[0])

    args = process_commandline()

    print(f"{app_name} args {argc} Load file: {args.filename} portfolio:{args.portfolio}")
    ii_csv = IICsv(args.filename, debug=True)

    save_divs_from_df(ii_csv.get_dividends(), args.portfolio)
    save_cash_from_df(ii_csv.get_cash(), args.portfolio)
    save_cash_from_df(ii_csv.get_interest(), args.portfolio)
    save_trades_from_df(ii_csv.get_trades(), args.portfolio)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
