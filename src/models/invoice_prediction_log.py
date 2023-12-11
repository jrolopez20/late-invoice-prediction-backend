from . import db
from sqlalchemy.dialects.postgresql import JSON

class InvoicePredictionLog(db.Model):
    __tablename__ = 'invoice_prediction_log'

    id = db.Column(db.Integer, primary_key=True)
    factoring_document_id = db.Column(db.Integer())
    request = db.Column(JSON)
    response = db.Column(db.Integer())

    def __init__(self, factoring_document_id, request, response):
        self.factoring_document_id = factoring_document_id
        self.request = request
        self.response = response

    def __repr__(self):
        return f"<Invoice prediction {self.factoring_document_id} -> {self.response}>"