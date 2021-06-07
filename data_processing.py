import pandas as pd

# reading in Diagnosis data and merging hospital location and diagnosis data
aprdrg_data = pd.read_csv('/Projects/4DG/APRDRG_IN2019.csv')
aprdrg_ID = pd.read_csv('/Projects/4DG/APRDRG_ID_2019_1.csv')
df_hosptlatlong = pd.read_csv('/Projects/4DG/HospLatLongID.csv')
city_ethnicity_data = pd.read_csv('/Projects/4DG/city_ethnicity_data.csv')

# cleaning up the data
hosp_ID_rename = df_hosptlatlong.rename(columns={"Hospital_ID": "HOSPITAL_ID"})
ethnicity_rename = city_ethnicity_data.rename(columns={"City_Name": "Hospital_City"})

# using pandas merge function by setting how='inner'
# this will merge the diagnosis data and diagnosis ID data sets into one

aprdrg_data_ID = pd.merge(aprdrg_data, aprdrg_ID,
                        on='APRDRG',
                        how='inner')


aprdrg_hosp_id_data = pd.merge(aprdrg_data_ID, hosp_ID_rename,
                  on='HOSPITAL_ID',
                  how='inner')

aprdrg_hospID_ethnicity = pd.merge(aprdrg_hosp_id_data, ethnicity_rename,
                                    on='Hospital_City',
                                    how='inner')


# this will create a new csv file we can work with
aprdrg_hospID_ethnicity.to_csv("APRDRG_HOSP_latlong_ethnicity.csv", index=False, encoding='utf-8-sig')
