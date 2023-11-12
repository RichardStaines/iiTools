# iiTools
This project is to create tools that I can use to process my trades, dividends and positions etc 
to help me monitor my trading ISA better.
 
Load from csv into a DB.
split between cash,dividends,trades, separate instruments dynamically.

support several portfolios / trading accounts

this will be integrated into my django Web app soon.

To create an empty DB: Run "alembic upgrade head" from a terminal

run load portfolios before loading the trading data

there is also a little aggregation / analyse tool to see my dividends etc by stock and by year
