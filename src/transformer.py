import pandas as pd
import numpy as np
import csv
from datetime import datetime


def from_dob_to_age(born):
    now = pd.Timestamp("now")
    return now.year - born.year - ((now.month, now.day) < (born.month, born.day))


def calc_payment_term(row):
    return (row.fecha_fin - row.fecha_inicio) / np.timedelta64(1, "D")


def transform(data):
    # Readind data
    df = pd.read_csv(
        "./src/model/all.csv",
        sep=",",
        parse_dates=["credito_fecha_inicio", "credito_fecha_fin", "fecha_pago"],
    )

    # Remove unnecesary columns
    df.drop(["cliente_sector", "cliente_regimen_fiscal"], axis=1, inplace=True)

    data["fecha_nacimiento"] = datetime.strptime(data["fecha_nacimiento"], "%Y/%m/%d")
    # Get the age of the client
    data["cliente_edad"] = from_dob_to_age(data["fecha_nacimiento"])

    df_input = pd.DataFrame(data, index=[0])

    # Transform dates column to proper format
    df_input["fecha_inicio"] = pd.to_datetime(df_input["fecha_inicio"])
    df_input["fecha_fin"] = pd.to_datetime(df_input["fecha_fin"])

    df_input = df_input.astype(
        {
            "porcentaje_adelanto": float,
            "factura_importe": float,
            "linea_limite": float,
            "pagador_rfc": str,
        }
    )

    print(df_input.info())

    # Build feature Payment term
    df_input["payment_term"] = df_input.apply(calc_payment_term, axis=1)

    # Build feature Number of total paid invoices
    def calc_number_total_paid_invoices(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
        ]
        return len(df_filtered.index)

    df_input["NumberTotalPaidInvoices"] = df_input.apply(
        calc_number_total_paid_invoices, axis=1
    )

    # Build feature Number of invoices that were paid late
    def calc_number_invoices_paid_late(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > df.credito_fecha_fin)
        ]
        return len(df_filtered.index)

    df_input["NumberInvoicesPaidLate"] = df_input.apply(
        calc_number_invoices_paid_late, axis=1
    )

    # Build feature Ratio of paid invoices that were late
    def calc_ratio_invoices_paid_late(row):
        if row.NumberTotalPaidInvoices == 0:
            return 0
        else:
            return row.NumberInvoicesPaidLate / row.NumberTotalPaidInvoices

    df_input["RatioInvoicesPaidLate"] = df_input.apply(
        calc_ratio_invoices_paid_late, axis=1
    )

    # Build feature Sum of the base amount of total paid invoices
    def calc_sum_amount_total_paid_invoices(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
        ]
        return df_filtered.factura_importe.sum()

    df_input["SumAmountTotalPaidInvoices"] = df_input.apply(
        calc_sum_amount_total_paid_invoices, axis=1
    )

    # Build feature Sum of the base amount of invoices that were paid late
    def calc_sum_amount_invoices_paid_late(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > df.credito_fecha_fin)
        ]
        return df_filtered.factura_importe.sum()

    df_input["SumAmountInvoicesPaidLate"] = df_input.apply(
        calc_sum_amount_invoices_paid_late, axis=1
    )

    # Build feature Ratio of sum of paid base amount that were late
    def calc_ratio_sum_amount_invoices_paid_late(row):
        if row.SumAmountTotalPaidInvoices == 0:
            return 0
        else:
            return row.SumAmountInvoicesPaidLate / row.SumAmountTotalPaidInvoices

    df_input["RatioSumAmountInvoicesPaidLate"] = df_input.apply(
        calc_ratio_sum_amount_invoices_paid_late, axis=1
    )

    # Build feature Average days late of paid invoices being late.
    def calc_avg_days_late_invoices_paid_late(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > df.credito_fecha_fin)
        ]
        df_filtered["DaysLate"] = df_filtered.fecha_pago - df_filtered.credito_fecha_fin

        if len(df_filtered.index) == 0:
            return 0
        else:
            mean = df_filtered.DaysLate.mean()
            return pd.to_timedelta([mean]).astype("timedelta64[D]")[0]

    df_input["AvgDaysLateInvoicesPaidLate"] = df_input.apply(
        calc_avg_days_late_invoices_paid_late, axis=1
    )

    # Build feature Number of total outstanding invoices
    def calc_number_total_outstanding_invoices(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > row.fecha_inicio)
        ]
        return len(df_filtered.index)

    df_input["NumberTotalOutstandingInvoices"] = df_input.apply(
        calc_number_total_outstanding_invoices, axis=1
    )

    # Build feature Number of outstanding invoices that were already late
    def calc_number_outstanding_late_invoices(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > df.credito_fecha_fin)
            & (df.fecha_pago > row.fecha_inicio)
        ]
        return len(df_filtered.index)

    df_input["NumberOutstandingLateInvoices"] = df_input.apply(
        calc_number_outstanding_late_invoices, axis=1
    )

    # Build feature Ratio of outstanding invoices that were late
    def calc_ratio_outstanding_late_invoices(row):
        if row.NumberTotalOutstandingInvoices == 0:
            return 0
        else:
            return (
                row.NumberOutstandingLateInvoices / row.NumberTotalOutstandingInvoices
            )

    df_input["RatioOutstandingLateInvoices"] = df_input.apply(
        calc_ratio_outstanding_late_invoices, axis=1
    )

    # Build feature Sum of the base amount of total outstanding invoices
    def calc_sum_amount_total_outstanding_invoices(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > row.fecha_inicio)
        ]
        return df_filtered.factura_importe.sum()

    df_input["SumAmountTotalOutstandingInvoices"] = df_input.apply(
        calc_sum_amount_total_outstanding_invoices, axis=1
    )

    # Build feature Sum of the base amount of outstanding invoices that were late
    def calc_sum_amount_outstanding_late_invoices(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > row.fecha_inicio)
            & (df.fecha_pago > df.credito_fecha_fin)
        ]
        return df_filtered.factura_importe.sum()

    df_input["SumAmountOutstandingLateInvoices"] = df_input.apply(
        calc_sum_amount_outstanding_late_invoices, axis=1
    )

    # Build feature Ratio of sum of outstanding base amount that were late
    def calc_ratio_sum_amount_outstanding_late_invoice(row):
        if row.SumAmountTotalOutstandingInvoices == 0:
            return 0
        else:
            return (
                row.SumAmountOutstandingLateInvoices
                / row.SumAmountTotalOutstandingInvoices
            )

    df_input["RatioSumAmountOutstandingLateInvoice"] = df_input.apply(
        calc_ratio_sum_amount_outstanding_late_invoice, axis=1
    )

    # Build feature Average days late of outstanding invoices being late.
    def calc_avg_days_late_outstanding_invoices_being_late(row):
        df_filtered = df[
            (df.pagador_rfc == row.pagador_rfc)
            & (df.credito_fecha_inicio < row.fecha_inicio)
            & (df.fecha_pago > df.credito_fecha_fin)
            & (df.fecha_pago > row.fecha_inicio)
        ]
        df_filtered["DaysLate"] = df_filtered.fecha_pago - df_filtered.credito_fecha_fin

        if len(df_filtered.index) == 0:
            return 0
        else:
            mean = df_filtered.DaysLate.mean()
            return pd.to_timedelta([mean]).astype("timedelta64[D]")[0]

    df_input["AvgDaysLateOutstandingInvoicesBeingLate"] = df_input.apply(
        calc_avg_days_late_outstanding_invoices_being_late, axis=1
    )

    # Remove unnecesary columns for prediction
    df_input.drop(
        ["fecha_nacimiento", "fecha_inicio", "fecha_fin", "pagador_rfc"],
        axis=1,
        inplace=True,
    )

    # print(df_input.head(), df_input.columns, len(df_input.columns))
    # input_data = df_input.values.tolist()

    return df_input
