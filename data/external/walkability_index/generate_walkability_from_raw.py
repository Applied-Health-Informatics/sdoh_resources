import pandas as pd 

df = pd.read_csv('/Users/hantswilliams/Downloads/EPA_SmartLocationDatabase_V3_Jan_2021_Final.csv')
df.columns

## print each column name
for col in df.columns:
    print(col)

## keep only where COUNTYFP is 59 (nassau) or 103 (suffolk) AND where stateFP is 36 (new york)
longisland = df[(df['STATEFP'] == 36)]
len(longisland)

## keep only where (df['COUNTYFP'] == 59) | (df['COUNTYFP'] == 103) & 
longisland = longisland[(longisland['COUNTYFP'] == 59) | (longisland['COUNTYFP'] == 103)]

## save to data/external/walkability_index/longisland_walkability.csv
longisland.to_csv('data/external/walkability_index/longisland_walkability.csv', index=False)