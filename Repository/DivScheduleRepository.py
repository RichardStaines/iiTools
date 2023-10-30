from Model.db import DividendSchedule, DataAccessLayer


class DivScheduleRepository:

    def __init__(self, data_access_layer : DataAccessLayer, debug=True):
        self.session = data_access_layer.create_session()
        self.debug = debug

    def clear_table(self):
        self.session.query(DividendSchedule).delete()
        self.session.commit()

    def get_div_schedule_list(self, year=None):
        query = self.session.query(DividendSchedule)

        if year is not None:
            query.where(DividendSchedule.payment_date.year == year)
        return query.all()

    def get_div_schedule(self, id):
        return self.session.query(DividendSchedule).filter(DividendSchedule.id == id).first()

    def update_div_schedule(self, id, updates_dict):
        rec = self.session.query(DividendSchedule).filter(DividendSchedule.id == id).first()
        for k,v in updates_dict:
            rec[k] = v
        self.session.commit()

    def save_from_df(self, df, clear_before_load=False):
        if clear_before_load:
            self.clear_table()
        rec_list = [DividendSchedule(instrument=row.Symbol,
                                     ex_div_date=row.ex_div_date,
                                     payment_date=row.payment_date,
                                     payment=row.payment,
                                     ) for row in df.itertuples()]
        if self.debug:
            print(rec_list)
        self.session.bulk_save_objects(rec_list)
        self.session.commit()
