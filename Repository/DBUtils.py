from Model.db import *


class DBUtil:

    def __init__(self, session, debug=True):
        self.session = session
        self.debug = debug

    def clear_tables(self):
        session.query(Cash).delete()
        session.query(Dividend).delete()
        session.query(Trade).delete()
        session.query(Instrument).delete()
        self.session.commit()

    def save_divs_from_df(self, df, portfolio):

        rec_list = [Dividend(instrument=div.Symbol,
                             sedol=div.Sedol,
                             description=div.Description,
                             amount=div.Credit,
                             payment_date=div.Datetime,
                             portfolio_id=portfolio.id
                             ) for div in df.itertuples()]
        if self.debug:
            print(rec_list)
        self.session.bulk_save_objects(rec_list)
        self.session.commit()

    def save_cash_from_df(self, df, portfolio):
        rec_list = [Cash(type=row.Type,
                         description=row.Description,
                         amount=row.Credit,
                         payment_date=row.Datetime,
                         portfolio_id=portfolio.id
                         ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        self.session.bulk_save_objects(rec_list)
        self.session.commit()

    def save_trades_from_df(self, df, portfolio):
        rec_list = [Trade(instrument=trd.Symbol,
                          sedol=trd.Sedol,
                          instrument_description=trd.Description,
                          buy_sell=trd.BuySell,
                          quantity=trd.Quantity,
                          price=trd.Price,
                          net_consideration=trd.Consideration,
                          trade_date=trd.Datetime,
                          reference=trd.Reference,
                          settle_date=trd.SettleDate,
                          portfolio_id=portfolio.id
                          ) for trd in df.itertuples()]
        if self.debug:
            print(rec_list)

        session.bulk_save_objects(rec_list)
        session.commit()

    def save_instruments_from_df(self, df):

        rec_list = [Instrument(code=row.Symbol,
                             sedol=row.Sedol,
                             description=row.Description,
                             ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)

        self.session.bulk_save_objects(rec_list)
        self.session.commit()
