import pandas as pd
import numpy as np
import joblib
import lime
import lime.lime_tabular


def predict(df_input):
    with open("./src/resources/model.joblib", "rb") as f:
        predictor = joblib.load(f)

    # BEGIN TESTING CODE
    # df = pd.read_csv("./src/resources/test.csv")

    # Remove features unseen at fit time:
    # df.drop(
    #     ["cliente_sector", "cliente_regimen_fiscal", "PaidTime"], axis=1, inplace=True
    # )

    # df_predict = df.iloc[0:1]
    # END TESTING CODE

    # Reorder input dataframe columns with model features
    df_input = df_input[predictor.feature_names_]
    prediction = predictor.predict(df_input)

    target_names = np.array(['before time', 'on time', '1-7 days late', '8-21 days late', 'More than 21 days late'])
    # target_names = np.array([1, 2, 3, 4, 5])

    X_train = pd.read_csv("./src/resources/all.csv", sep=",")

    # Remove unnecesary columns
    X_train.drop(
        [
            "cliente_sector",
            "cliente_regimen_fiscal",
            "cliente_ocupacion",
            "pagador_scian_nombre",
            "credito_fecha_inicio",
            "credito_fecha_fin",
            "fecha_pago",
            "pagador_rfc",
            "PaidTime",
        ],
        axis=1,
        inplace=True,
    )

    lime_explainer = lime.lime_tabular.LimeTabularExplainer(
        training_data=np.array(X_train),
        feature_names=X_train.columns,
        class_names=target_names,
        mode="classification",
    )

    testing_row = df_input.iloc[0]

    print(testing_row, len(testing_row))

    lime_instance_expl = lime_explainer.explain_instance(
        data_row=testing_row,
        predict_fn=predictor.predict_proba,
        num_features=6,
        top_labels=1,
    )

    explainer_html = lime_instance_expl.as_html()

    
    # Representing the explanation
    # lime_instance_expl.show_in_notebook(show_table=True, show_all=False)

    # Representing the explanation
    # lime_instance_expl.

    return {
         "prediction":  prediction.tolist(),
         "explainer_html":  explainer_html
    }
