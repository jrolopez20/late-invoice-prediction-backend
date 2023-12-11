from flask import Blueprint, request, jsonify, current_app
from flask_cors import cross_origin
from src import transformer, predictor
from src.models import db
from src.models.invoice_prediction_log import InvoicePredictionLog
import os

routes_blueprint = Blueprint(
    "main",
    __name__,
)


def is_valid(api_key):
    return api_key == current_app.config["API_KEY"]

@routes_blueprint.route("/", methods=["GET"])
def home():
    return "Nothing to show"


@routes_blueprint.route("/predict", methods=["POST"])
@cross_origin()
def predict_late_invoice():
    if not is_valid(request.headers.get('API-KEY')):
        return {"message": "You must provide a valid api key"}, 401

    params = request.get_json(force=True)
    req = dict((k, params[k]) for k in ['factura_importe', 'fecha_fin', 'fecha_inicio', 'fecha_nacimiento', 'linea_limite', 'pagador_rfc', 'porcentaje_adelanto']
           if k in params)

    data = transformer.transform(req)

    result = predictor.predict(data)

    log = InvoicePredictionLog(params['factoring_document_id'], params, result['prediction'][0])
    db.session.add(log)
    db.session.commit()

    return result
