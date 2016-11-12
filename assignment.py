import pandas as pd
df=pd.read_csv ("c:\kisanhub.csv", index_col=['record_ts'], parse_dates=['record_ts'])
#print df
# for missing values, linear interpolation method
df=df.reindex(pd.date_range("01/01/2014", "31/05/2016",freq='H'), fill_value="Nan")
df=df.astype(float)
df=df.interpolate(method='linear', axis=0).ffill().bfill()
print df
maximum=df.resample('24H').max()
minimum=df.resample('24H').min()
#print maximum
#print minimum
mean=(maximum+minimum)/2
#print mean
target = open("test.csv", 'w')
target.truncate()
mean.to_csv('test.csv', mode='a', header=False)
user_cols=['date', 'value']
dm=pd.read_csv ("test.csv", header=None, names=user_cols)
dm.head()


