import os
import pandas as pd
import numpy
from datetime import datetime, timedelta
#import great_expectations as ge

# Read all csv files and concat into a dataframe.
# Get csv file name in ConsumptionData folder
path = "Data/ConsumptionData/"
file_list = os.listdir(path)
name_list = []
for filename in file_list:
    #print(filename)
    if filename.endswith(".csv"):
        #table_list.append(pd.read_csv(filename,sep="|"))
        name_list.append(os.path.splitext(filename)[0])
print(name_list)
len(name_list)

nmi_info = pd.read_csv("Data/nmi_info.csv")
nmi_info.head()

# Read CSV into Pandas Dataframe
NMIA3 = pd.read_csv(path + "NMIA3" + ".csv")
NMIA2 = pd.read_csv(path + "NMIA2" + ".csv")
NMIM1 = pd.read_csv(path + "NMIM1" + ".csv")
NMIA1 = pd.read_csv(path + "NMIA1" + ".csv")
NMIS3 = pd.read_csv(path + "NMIS3" + ".csv")
NMIS2 = pd.read_csv(path + "NMIS2" + ".csv")
NMIK4 = pd.read_csv(path + "NMIK4" + ".csv")
NMIS1 = pd.read_csv(path + "NMIS1" + ".csv")
NMIR1 = pd.read_csv(path + "NMIR1" + ".csv")
NMIG1 = pd.read_csv(path + "NMIG1" + ".csv")
NMIR2 = pd.read_csv(path + "NMIR2" + ".csv")
NMIG2 = pd.read_csv(path + "NMIG2" + ".csv")
NMIA3["Nmi"] = "NMIA3"
NMIA2["Nmi"] = "NMIA2"
NMIM1["Nmi"] = "NMIM1"
NMIA1["Nmi"] = "NMIA1"
NMIS3["Nmi"] = "NMIS3"
NMIS2["Nmi"] = "NMIS2"
NMIK4["Nmi"] = "NMIK4"
NMIS1["Nmi"] = "NMIS1"
NMIR1["Nmi"] = "NMIR1"
NMIG1["Nmi"] = "NMIG1"
NMIR2["Nmi"] = "NMIR2"
NMIG2["Nmi"] = "NMIG2"
NMIG2.head()


nmi_all = pd.concat([NMIA2,NMIM1,NMIA1,NMIS3,NMIS2,NMIK4,NMIS1,NMIR1,NMIG1,NMIR2,NMIG2,NMIA3])
nmi_all = nmi_all.reset_index(drop=True)

# Inspect Data and Unified Unit

# Check how many unique values in each columns
uniqueValues = nmi_all.nunique() 
print(uniqueValues)

#Update all the Unit to kWh and update the Quantity value accordingly and round to two decimal.
nmi_all.loc[nmi_all["Unit"] =="Mwh",'Quantity'] = nmi_all["Quantity"] * 1000
nmi_all["Unit"] = "kWh"
nmi_all.round({"Quantity": 2})

# Check the null value in each column
nmi_all.isnull().sum()

# conver string to datetime
nmi_all["AESTTime"] = pd.to_datetime(nmi_all["AESTTime"])

# Join Consumption data and nmi_info data together
nmi_all_info = pd.merge(nmi_all, nmi_info, how='left', on='Nmi')
# nmi_all_info["Year"]=pd.DatetimeIndex(nmi_all_info["AESTTime"]).year
# nmi_all_info["Year"] = nmi_all_info["Year"].astype(int)
nmi_all_info.head()
#nmi_all_info.dtypes

Interval = AESTnulldf["Interval"].unique()
nmi_all_info["Interval"] = nmi_all_info["Interval"].fillna(0).astype(int)
#nmi_all_info['AESTTime'] = nmi_all_info['AESTTime'] + pd.Series([datetime.timedelta(minutes=x) for x in wait_min])
for ind, row in nmi_all_info.iterrows():
    if nmi_all_info.loc[ind,"AESTTime"] is pd.NaT:
        nmi_all_info.loc[ind,"AESTTime"] = nmi_all_info.loc[ind-1,"AESTTime"] + timedelta(minutes=30)

# Checking dataframe, state information is missing due to NMIK4 information is missing from nmi_info.csv file
nmi_all_info.isnull().sum()

#Find out the DST time period and convert AEST Time to local time
# Grab the max and min year in NMI dataframe
import datetime
start_time = nmi_all_info["AESTTime"].min()
startYear = start_time.year
finish_time = nmi_all_info["AESTTime"].max()
finishYear = finish_time.year
print(startYear)
print(finishYear)

from datetime import datetime, timedelta
# input year and month
yearMonthStart = f'{startYear}-10'
  
# getting date of first Sunday in Oct.
dst_start_time = numpy.busday_offset(yearMonthStart, 0, 
                           roll='forward', 
                           weekmask='Sun')
# input year and month
yearMonthFinish = f'{finishYear}-04'
  
# getting date of first Sunday in Apr.
dst_finish_time = numpy.busday_offset(yearMonthFinish, 0, 
                           roll='forward', 
                           weekmask='Sun')

dst_start_dt = datetime.strptime(f'{dst_start_time}  02:00:00', '%Y-%m-%d %H:%M:%S')
dst_finish_dt = datetime.strptime(f'{dst_finish_time}  03:00:00', '%Y-%m-%d %H:%M:%S')
print(dst_start_dt)
print(dst_finish_dt)

# create dataframe with NMI in VIC, NSW, and WA which need to change to local time
df_dst = nmi_all_info.loc[(nmi_all_info["State"]=="VIC") | (nmi_all_info["State"]=="NSW")]
df_dst.loc[(df_dst["AESTTime"] >= dst_start_dt)&(df_dst["AESTTime"] < dst_finish_dt),'LocalTime'] = df_dst["AESTTime"] + timedelta(hours=1)
df_wa = nmi_all_info.loc[(nmi_all_info["State"]=="WA")]
df_wa['LocalTime'] = df_wa["AESTTime"] - timedelta(hours=2)
df_qld = nmi_all_info.loc[(nmi_all_info["State"]=="QLD")]
df_qld["LocalTime"] = df_qld["AESTTime"]
#df_wa['LocalTime'] = df_dst["AESTTime"] - timedelta(hours=2)
df_dst.head()

# Fill no time difference fild with AEST Time.
nmi_local_time = pd.concat([df_dst,df_wa,df_qld])
nmi_local_time.LocalTime.fillna(nmi_local_time.AESTTime, inplace=True)
nmi_local_time["Year"]=pd.DatetimeIndex(nmi_local_time["LocalTime"]).year
#nmi_local_time["Year"] = nmi_local_time["Year"].fillna(0).astype(int)

#Data Validation

import great_expectations as ge
import os
import numpy as np
import seaborn as sns
import os
import datetime
%matplotlib inline

nmi_local_time.info()

nmi_local_time.describe()

#Seperate date and time

nmi_local_time["LocalDate"]= nmi_local_time["LocalTime"].dt.date
nmi_local_time["LocalTime"]= nmi_local_time["LocalTime"].dt.time
nmi_local_time.head(3)

# When was the highest Energy Consumption, which NMI, what time, and which year

nmi_local_time[nmi_local_time["Quantity"] == nmi_local_time["Quantity"].max()]
nmi_local_time[nmi_local_time["Quantity"] == nmi_local_time["Quantity"].min()]

# Plot and Data visualization
sns.distplot(nmi_local_time["Quantity"])


# Check how many years are unique
nmi_local_time["Year"].unique()

countLT = (nmi_local_time["LocalTime"] == 0).sum()
countQ = (nmi_local_time["Quantity"] == 0).sum()
print(countQ)

nmi_local_time.to_csv('NMI_Consumption.csv', index=False)


