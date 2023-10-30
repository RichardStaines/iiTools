from Model.db import Portfolio, DataAccessLayer


class PortfolioRepository:

    def __init__(self, data_access_layer : DataAccessLayer, debug=True):
        self.session = data_access_layer.create_session()
        self.debug = debug

    def clear_table(self):
        self.session.query(Portfolio).delete()
        self.session.commit()

    def get_portfolio(self, name):
        return self.session.query(Portfolio).filter(Portfolio.name == name).first()

    def get_portfolio_list(self):
        return self.session.query(Portfolio)

    def update_portfolio(self, id, updates_dict):
        rec = self.session.query(Portfolio).filter(Portfolio.id == id).first()
        for k,v in updates_dict:
            rec[k] = v
        self.session.commit()

    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        rec_list = [Portfolio(name=row.Name,
                              description=row.Description,
                             ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        self.session.bulk_save_objects(rec_list)
        self.session.commit()
