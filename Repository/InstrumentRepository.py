from Model.db import Instrument


class InstrumentRepository:

    def __init__(self, data_access_layer, debug=True):
        self.session = data_access_layer.create_session()
        self.debug = debug

    def clear_table(self):
        self.session.query(Instrument).delete()
        self.session.commit()

    def get_instrument_by_code(self, code):
        return self.session.query(Instrument).filter(Instrument.code == code).first()

    def get_instrument(self, id):
        return self.session.query(Instrument).filter(Instrument.id == id).first()

    def get_instrument_list(self):
        return self.session.query(Instrument)

    def update_instrument(self, id, updates_dict):
        rec = self.session.query(Instrument).filter(Instrument.id == id).first()
        for k,v in updates_dict:
            rec[k] = v
        self.session.commit()

    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        rec_list = [Instrument(code=row.Symbol,
                             sedol=row.Sedol,
                             description=row.Description,
                             ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        self.session.bulk_save_objects(rec_list)
        self.session.commit()
