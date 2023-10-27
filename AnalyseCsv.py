import sys
import os

from Utils.iiCSV import IICsv


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

    ii_csv = IICsv(filename, debug=True)
    # interest, divs, trades, cash = load_csv(filename)

    # my divs each year...
    IICsv.sum_by_year(ii_csv.get_interest(), "Interest")

    IICsv.sum_by_year(ii_csv.get_dividends(), "Divs by Year")
    IICsv.sum_by_symbol_and_year(ii_csv.get_dividends(), "Divs by Symbol and Year")
    IICsv.sum_by_symbol(ii_csv.get_dividends(), 'Divs by Symbol')

    IICsv.sum_by_year(ii_csv.get_cash(), "Cash")

    # my trading activity
    # The Qty doesn't always make sense as the csv file has no starting positions and nothing before 2021
    IICsv.sum_by_symbol(ii_csv.get_trades(), "Trades by Symbol", include_qty=True)
    IICsv.sum_by_symbol_and_year(ii_csv.get_trades(), "Trades by Symbol and Year", include_qty=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
