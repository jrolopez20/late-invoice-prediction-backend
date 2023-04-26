from flask import Flask, request, jsonify
from flask_cors import cross_origin
import transformer
import predictor

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Nothing to show"


@app.route("/predict", methods=["POST"])
@cross_origin()
def predict_home_price():
    params = request.get_json(force=True)

    data = transformer.transform(params)
    
    result = predictor.predict(data)
    
    response = {
        "prediction":  result.tolist()
    }
    # response = jsonify(result.tolist())

    return response


if __name__ == "__main__":
    print("Starting Python Flask server for Late invoice prediction...")
    app.run(debug=True)
