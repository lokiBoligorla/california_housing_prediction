
import pickle
from flask import Flask, request, jsonify, render_template
import numpy as np

app = Flask(__name__)

# Load the trained model and scaler
with open("regmodel.pkl", "rb") as file:
    regmodel = pickle.load(file)

with open("scaling.pkl", "rb") as file:
    scalar = pickle.load(file)


# California Housing dataset feature order
FEATURES = [
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude"
]


@app.route("/")
def home():
    return render_template("home.html")


# API prediction
@app.route("/predict_api", methods=["POST"])
def predict_api():

    data = request.get_json()

    input_data = [float(data["data"][feature]) for feature in FEATURES]

    final_input = np.array(input_data).reshape(1, -1)

    scaled_data = scalar.transform(final_input)

    prediction = regmodel.predict(scaled_data)[0]

    return jsonify({
        "prediction": float(prediction)
    })


# HTML form prediction
@app.route("/predict", methods=["POST"])
def predict():

    try:
        data = [
            float(request.form[feature])
            for feature in FEATURES
        ]

        final_input = np.array(data).reshape(1, -1)

        scaled_data = scalar.transform(final_input)

        prediction = regmodel.predict(scaled_data)[0]

        return render_template(
            "home.html",
            prediction_text="The House Price Prediction is: {:.4f} ($100,000 units)".format(prediction)
        )

    except (ValueError, KeyError) as e:
        return render_template(
            "home.html",
            prediction_text=f"Invalid input: {e}"
        )


if __name__ == "__main__":
    app.run(debug=True)
