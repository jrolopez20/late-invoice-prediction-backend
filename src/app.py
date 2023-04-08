from flask import Flask, request, jsonify
import transformer
import predictor

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Nothing to show"


@app.route("/predict", methods=["POST"])
def predict_home_price():
    params = request.get_json(force=True)

    data = transformer.transform(params)
    
    result = predictor.predict(data)

    response = jsonify(result.tolist())
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response


if __name__ == "__main__":
    print("Starting Python Flask server for Late invoice prediction...")
    app.run()
