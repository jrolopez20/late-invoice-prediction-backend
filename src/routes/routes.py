from flask import Blueprint, request, jsonify
from flask_cors import cross_origin
from src import transformer, predictor
from src.models import db
from src.models.invoice_prediction_log import InvoicePredictionLog
import os
routes_blueprint = Blueprint('main', __name__,)

@routes_blueprint.route('/', methods=["GET"])
def home():
    return "Nothing to show"


@routes_blueprint.route("/predict", methods=["POST"])
@cross_origin()
def predict_late_invoice(): 
    params = request.get_json(force=True)
    
    req = dict((k, params[k]) for k in ['factura_importe', 'fecha_fin', 'fecha_inicio', 'fecha_nacimiento', 'linea_limite', 'pagador_rfc', 'porcentaje_adelanto']
           if k in params)
    
    data = transformer.transform(req)

    result = predictor.predict(data)
        
    log = InvoicePredictionLog(params['folio'], params, result['prediction'][0])
    db.session.add(log)
    db.session.commit()

    return result