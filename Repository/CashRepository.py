from Model.db import Cash


class CashRepository:

    def __init__(self, data_access_layer, debug=True):
        self.session = data_access_layer.create_session()
        self.debug = debug

    def clear_table(self):
        self.session.query(Cash).delete()
        self.session.commit()

    def get_cash_list(self, year=None):
        query = self.session.query(Cash)

        if year is not None:
            query.where(Cash.payment_date.year == year)
        return query.all()

    def get_cash(self, id):
        return self.session.query(Cash).filter(Cash.id == id).first()

    def update_cash(self, id, updates_dict):
        rec = self.session.query(Cash).filter(Cash.id == id).first()
        for k,v in updates_dict:
            rec[k] = v
        self.session.commit()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
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
