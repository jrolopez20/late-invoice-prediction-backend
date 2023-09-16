from . import db
from sqlalchemy.dialects.postgresql import JSON

class InvoicePredictionLog(db.Model):
    __tablename__ = 'invoice_prediction_log'

    id = db.Column(db.Integer, primary_key=True)
    folio = db.Column(db.String(20))
    request = db.Column(JSON)
    response = db.Column(db.Integer())

    def __init__(self, folio, request, response):
        self.folio = folio
        self.request = request
        self.response = response

    def __repr__(self):
        return f"<Invoice prediction {self.folio} -> {self.response}>"