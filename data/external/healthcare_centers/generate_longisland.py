import pandas as pd

df = pd.read_csv('data/external/healthcare_centers/Health_Facility_General_Information_20240610.csv')

df.columns

df['Facility County'].unique()

## keep only where COUNTY is Nassau or Suffolk
longisland = df[(df['Facility County'] == 'Nassau') | (df['Facility County'] == 'Suffolk')]

len(longisland)

## save to data/external/healthcare_centers/longisland_healthcare_centers.csv
longisland.to_csv('data/external/healthcare_centers/longisland_healthcare_centers.csv', index=False)