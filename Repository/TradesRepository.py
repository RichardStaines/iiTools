from Model.db import Trade, DataAccessLayer


class TradeRepository:

    def __init__(self, data_access_layer : DataAccessLayer, debug=True):
        self.session = data_access_layer.create_session()
        self.debug = debug

    def clear_table(self):
        self.session.query(Trade).delete()
        self.session.commit()

    def get_trade_list(self, year=None):
        query = self.session.query(Trade)

        if year is not None:
            query.where(Trade.payment_date.year == year)
        return query.all()

    def get_trade(self, id):
        return self.session.query(Trade).filter(Trade.id == id).first()

    def update_dividend(self, id, updates_dict):
        rec = self.session.query(Trade).filter(Trade.id == id).first()
        for k,v in updates_dict:
            rec[k] = v
        self.session.commit()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
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
        self.session.bulk_save_objects(rec_list)
        self.session.commit()
