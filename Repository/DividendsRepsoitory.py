from Model.db import Dividend


class DividendRepository:

    def __init__(self, session, debug=True):
        self.session = session
        self.debug = debug

    def clear_table(self):
        self.session.query(Dividend).delete()
        self.session.commit()

    def get_dividend_list(self, year=None):
        query = self.session.query(Dividend)

        if year is not None:
            query.where(Dividend.payment_date.year == year)
        return query.all()

    def get_dividend(self, id):
        return self.session.query(Dividend).filter(Dividend.id == id).first()

    def update_dividend(self, id, updates_dict):
        rec = self.session.query(Dividend).filter(Dividend.id == id).first()
        for k,v in updates_dict:
            rec[k] = v
        self.session.commit()

    def save_from_df(self, df, portfolio, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
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
