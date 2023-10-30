import sys
import os
import argparse
import pandas as pd

from Repository.DivScheduleRepository import DivScheduleRepository
from Model.db import *


def process_commandline():
    parser = argparse.ArgumentParser(
        usage="%(prog)s [-reload] <csv-filename>\n-reload will empty the tables before loading"
    )
    parser.add_argument(
        "-reload", action=argparse.BooleanOptionalAction
    )
    parser.add_argument("filename")  # positional parameter so mandatory
    args = parser.parse_args()
    print(args)

    return args


def load_csv(filename, debug=False):
    df = pd.read_csv(filename, keep_default_na=True)
    df['ex_div_date'] = pd.to_datetime(df['ex_div_date'], format='%d/%m/%Y', errors='coerce')
    df['payment_date'] = pd.to_datetime(df['payment_date'], format='%d/%m/%Y', errors='coerce')
    if debug:
        print(df.columns)
    return df


def main(argc, argv):
    app_name = os.path.basename(sys.argv[0])

    args = process_commandline()
    print(f"{app_name} args {argc} Load file: {args.filename}")

    df = load_csv(args.filename, debug=False)
    data_access_layer.connect()
    db = DivScheduleRepository(data_access_layer, debug=True)
    db.save_from_df(df, args.reload)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
