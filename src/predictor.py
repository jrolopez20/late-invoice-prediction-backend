import pandas as pd
import joblib


def predict(df_input):
    with open("./src/model/model.joblib", "rb") as f:
        predictor = joblib.load(f)

    # BEGIN TESTING CODE
    # df = pd.read_csv("./src/model/test.csv")

    # Remove features unseen at fit time:
    # df.drop(
    #     ["cliente_sector", "cliente_regimen_fiscal", "PaidTime"], axis=1, inplace=True
    # )

    # df_predict = df.iloc[0:1]
    # END TESTING CODE

    # Reorder input dataframe columns with model features
    df_input = df_input[predictor.feature_names_]
    prediction = predictor.predict(df_input)

    return prediction
