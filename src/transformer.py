import pandas as pd
import numpy as np
import csv
from datetime import datetime


def transform(data):
    result = [1, 4564, 4, 0]
    return result


# def transform(data):
#     # Readind data
#     s3_client = boto3.client("s3")
#     bucket_name = 'finance-factoring-ml-dev'
#     object_key = "data/all.csv"

#     csv_object = s3_client.get_object(Bucket=bucket_name, Key=object_key)

#     file_content = csv_object['Body'].read().decode('utf-8').splitlines()

#     csv_reader = csv.reader(file_content)
#     headers = next(csv_reader)

#     df = pd.DataFrame(csv_reader, index = None, columns=headers)

#     # Remove unnecesary columns
#     df.drop("RFCPagador", axis=1, inplace=True)
#     df.drop("Moneda", axis=1, inplace=True)
#     df.drop("DepositoInicial", axis=1, inplace=True)
#     df.drop("Intereses", axis=1, inplace=True)

#     # Fix columns format
#     df = df.astype({
#         'Fecha': float,
#         'FechaVencimiento': float,
#         'RFCCliente': str,
#         'Monto': float,
#         'FechaPago': float,
#     })

#     df_input = pd.DataFrame(data, columns=['Fecha', 'RFCCliente', 'FechaVencimiento', 'Monto'])

#     # Transform dates column to proper format
#     df_input['Fecha'] = pd.to_datetime(df_input['Fecha'])
#     df_input['FechaVencimiento'] = pd.to_datetime(df_input['FechaVencimiento'])

#     def calc_timeDelta(_df, col):
#         return (_df[col] - datetime(2016, 1, 1)) / np.timedelta64(1, 'D')

#     # Convert datetime columns to numerical values
#     df_input["Fecha"] = calc_timeDelta(df_input, "Fecha")
#     df_input["FechaVencimiento"] = calc_timeDelta(df_input, "FechaVencimiento")

#     # Build feature Payment term
#     def calc_payment_term(row):
#         return row.FechaVencimiento - row.Fecha

#     df_input['PaymentTerm'] = df_input.apply(calc_payment_term, axis=1)

#     # Build feature Number of total paid invoices
#     def calc_number_total_paid_invoices(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha)]

#         return len(df_filtered.index)

#     df_input['NumberTotalPaidInvoices'] = df_input.apply(calc_number_total_paid_invoices, axis=1)

#     # Build feature Number of invoices that were paid late
#     def calc_number_invoices_paid_late(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha)  & (df.FechaPago > df.FechaVencimiento)]

#         return len(df_filtered.index)

#     df_input['NumberInvoicesPaidLate'] = df_input.apply(calc_number_invoices_paid_late, axis=1)

#     # Build feature Ratio of paid invoices that were late
#     def calc_ratio_invoices_paid_late(row):
#         if row.NumberTotalPaidInvoices == 0:
#             return 0
#         else:
#             return row.NumberInvoicesPaidLate / row.NumberTotalPaidInvoices

#     df_input['RatioInvoicesPaidLate'] = df_input.apply(calc_ratio_invoices_paid_late, axis=1)

#     # Build feature Sum of the base amount of total paid invoices
#     def calc_sum_amount_total_paid_invoices(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha)]

#         return df_filtered.Monto.sum()

#     df_input['SumAmountTotalPaidInvoices'] = df_input.apply(calc_sum_amount_total_paid_invoices, axis=1)

#     # Build feature Sum of the base amount of invoices that were paid late
#     def calc_sum_amount_invoices_paid_late(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > df.FechaVencimiento)]

#         return df_filtered.Monto.sum()

#     df_input['SumAmountInvoicesPaidLate'] = df_input.apply(calc_sum_amount_invoices_paid_late, axis=1)

#     # Build feature Ratio of sum of paid base amount that were late
#     def calc_ratio_sum_amount_invoices_paid_late(row):
#         if row.SumAmountTotalPaidInvoices == 0:
#             return 0
#         else:
#             return row.SumAmountInvoicesPaidLate / row.SumAmountTotalPaidInvoices

#     df_input['RatioSumAmountInvoicesPaidLate'] = df_input.apply(calc_ratio_sum_amount_invoices_paid_late, axis=1)

#     # Build feature Average days late of paid invoices being late.
#     def calc_avg_days_late_invoices_paid_late(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > df.FechaVencimiento)]

#         df_filtered['DaysLate'] = df_filtered['FechaPago'] - df_filtered['FechaVencimiento']

#         if len(df_filtered.index) == 0:
#             return 0
#         else:
#             return df_filtered.DaysLate.mean()

#     df_input['AvgDaysLateInvoicesPaidLate'] = df_input.apply(calc_avg_days_late_invoices_paid_late, axis=1)

#     # Build feature Number of total outstanding invoices
#     def calc_number_total_outstanding_invoices(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > row.Fecha)]

#         return len(df_filtered.index)

#     df_input['NumberTotalOutstandingInvoices'] = df_input.apply(calc_number_total_outstanding_invoices, axis=1)

#     # Build feature Number of outstanding invoices that were already late
#     def calc_number_outstanding_late_invoices(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > df.FechaVencimiento) & (df.FechaPago > row.Fecha)]

#         return len(df_filtered.index)

#     df_input['NumberOutstandingLateInvoices'] = df_input.apply(calc_number_outstanding_late_invoices, axis=1)

#     # Build feature Ratio of outstanding invoices that were late
#     def calc_ratio_outstanding_late_invoices(row):
#         if row.NumberTotalOutstandingInvoices == 0:
#             return 0
#         else:
#             return row.NumberOutstandingLateInvoices / row.NumberTotalOutstandingInvoices

#     df_input['RatioOutstandingLateInvoices'] = df_input.apply(calc_ratio_outstanding_late_invoices, axis=1)

#     # Build feature Sum of the base amount of total outstanding invoices
#     def calc_sum_amount_total_outstanding_invoices(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > row.Fecha)]

#         return df_filtered.Monto.sum()

#     df_input['SumAmountTotalOutstandingInvoices'] = df_input.apply(calc_sum_amount_total_outstanding_invoices, axis=1)

#     # Build feature Sum of the base amount of outstanding invoices that were late
#     def calc_sum_amount_outstanding_late_invoices(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > row.Fecha) & (df.FechaPago > df.FechaVencimiento)]

#         return df_filtered.Monto.sum()

#     df_input['SumAmountOutstandingLateInvoices'] = df_input.apply(calc_sum_amount_outstanding_late_invoices, axis=1)

#     # Build feature Ratio of sum of outstanding base amount that were late
#     def calc_ratio_sum_amount_outstanding_late_invoice(row):
#         if row.SumAmountTotalOutstandingInvoices == 0:
#             return 0
#         else:
#             return row.SumAmountOutstandingLateInvoices / row.SumAmountTotalOutstandingInvoices

#     df_input['RatioSumAmountOutstandingLateInvoice'] = df_input.apply(calc_ratio_sum_amount_outstanding_late_invoice, axis=1)

#     # Build feature Average days late of outstanding invoices being late.
#     def calc_avg_days_late_outstanding_invoices_being_late(row):
#         df_filtered = df[(df.RFCCliente == row.RFCCliente) & (df.Fecha < row.Fecha) & (df.FechaPago > df.FechaVencimiento) & (df.FechaPago > row.Fecha)]

#         df_filtered['DaysLate'] = df_filtered['FechaPago'] - df_filtered['FechaVencimiento']

#         if len(df_filtered.index) == 0:
#             return 0
#         else:
#             return df_filtered.DaysLate.mean()

#     df_input['AvgDaysLateOutstandingInvoicesBeingLate'] = df_input.apply(calc_avg_days_late_outstanding_invoices_being_late, axis=1)

#     # Remove RFCCliente, Fecha and FechaVencimiento features because it's no longer needed
#     df_input.drop("RFCCliente", axis=1, inplace=True)
#     df_input.drop("Fecha", axis=1, inplace=True)
#     df_input.drop("FechaVencimiento", axis=1, inplace=True)

#     input_data = df_input.values.tolist()

#     return input_data
