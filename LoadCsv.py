import sys
import os
import argparse

from Repository.CashRepository import CashRepository
from Utils.iiCSV import IICsv
from Repository.DBUtils import DBUtil
from Model.db import *
from Repository.PortfolioRepository import PortfolioRepository
from Repository.InstrumentRepository import  InstrumentRepository

def process_commandline():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-reload] -p <portfolio> <II-csv-filename>\n-reload will empty the tables before loading"
    )
    parser.add_argument(
        "-p", "--portfolio", default=''
    )
    parser.add_argument(
        "-reload", action=argparse.BooleanOptionalAction
    )
    parser.add_argument("filename")  # positional parameter so mandatory
    args = parser.parse_args()
    print(args)

    return args


def main(argc, argv):
    app_name = os.path.basename(sys.argv[0])

    args = process_commandline()
    print(f"{app_name} args {argc} Load file: {args.filename} portfolio:{args.portfolio}")

    portfolio_repo = PortfolioRepository(session, debug=True)
    portfolio = portfolio_repo.get_portfolio(args.portfolio)
    if portfolio is None:
        print(f"portfolio:{args.portfolio} is not registered")
        exit(1)

    ii_csv = IICsv(args.filename, debug=True)

    instRepo = InstrumentRepository(session, debug=False)
    cashRepo = CashRepository(session, debug=False)
    dbutil = DBUtil(session, debug=True)

    if args.reload:
        print("Reload Request")
        dbutil.clear_tables()

    print(f"Instruments={ii_csv.get_instruments()}")
    instRepo.save_from_df(ii_csv.get_instruments(), args.reload)

    dbutil.save_divs_from_df(ii_csv.get_dividends(), portfolio)
    cashRepo.save_from_df(ii_csv.get_cash(), portfolio, args.reload)
    cashRepo.save_from_df(ii_csv.get_interest(), portfolio, args.reload)
    dbutil.save_trades_from_df(ii_csv.get_trades(), portfolio)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
