import pandas as pd
import numpy as np

def show_operation_hours(nmi):
    # Group by dataframe and find the median, std and max of Quantity column
    nmi_data = pd.read_csv("NMI_Consumption.csv")
    nmi_aggregate = nmi_data[["Quantity","Nmi"]]
    nmi_median = nmi_aggregate.groupby("Nmi").median()
    nmi_std = nmi_aggregate.groupby("Nmi").std()
    max_opt = nmi_median + nmi_std*4
    min_opt = nmi_median - nmi_std 
    max_opt.reset_index(inplace=True)
    min_opt.reset_index(inplace=True)
    filt = (max_opt["Nmi"] == f"{nmi}")
    max_qty = max_opt[filt]["Quantity"].values[0]
    min_qty = min_opt[filt]["Quantity"].values[0]
    nmi_operating_hour= nmi_data.loc[(nmi_data['Nmi'] == nmi) & (nmi_data['Quantity']>= min_qty) & (nmi_data['Quantity'] <= max_qty)]
    op_hours = (nmi_operating_hour["Interval"].sum())/60

    return op_hours

show_operation_hours("NMIA1")