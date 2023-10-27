import sys
import os
import argparse

from Utils.iiCSV import IICsv
from Utils.DBUtils import DBUtil
from Model.db import *


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
    ii_csv = IICsv(args.filename, debug=False)

    dbutil = DBUtil(session, debug=True)
    dbutil.save_divs_from_df(ii_csv.get_dividends(), args.portfolio)
    dbutil.save_cash_from_df(ii_csv.get_cash(), args.portfolio)
    dbutil.save_cash_from_df(ii_csv.get_interest(), args.portfolio)
    dbutil.save_trades_from_df(ii_csv.get_trades(), args.portfolio)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
