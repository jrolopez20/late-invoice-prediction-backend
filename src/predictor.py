import pandas as pd
import joblib


def predict(items):
    with open("./src/model/model.joblib", "rb") as f:
        predictor = joblib.load(f)

    # TODO BEGIN Just for testing purpose
    df = pd.read_csv("./src/model/test.csv")

    # Remove features unseen at fit time:
    df.drop(
        ["cliente_sector", "cliente_regimen_fiscal", "PaidTime"], axis=1, inplace=True
    )

    df_predict = df.iloc[0:1]
    # END testing code

    result = predictor.predict(df_predict)
    
    return result
