import pandas as pd
import csv

# Reading weather file of .csv format
Reading_weatherfile= pd.read_csv ("kisanhub.csv",index_col=['record_ts'],parse_dates=['record_ts'])

# To find missing values using Linear Interpolation method
def Finding_MissingWeatherData (Weatherfile, Starting_Year, Final_Year):
    Starting_Year= convert_StringtoTimestamp(Starting_Year)
    Final_Year= convert_StringtoTimestamp(Final_Year)
    DateRange= pd.date_range(Starting_Year, Final_Year,freq='H')
    Reindex_WeatherData= Weatherfile.reindex(DateRange, fill_value="Nan")
    ConvertDataType=Reindex_WeatherData.astype(float)
    Corrected_WeatherFile=ConvertDataType.interpolate(method='linear')
    return Corrected_WeatherFile
  
# Resample data sets in 24hours group
def Resample_data(file):
    return file.resample('24H')

# To find Maximum Temperature
def Maximum_Temp(data):
    return data.max()

# To find Minimum Temperature
def Minimum_Temp(data):
    return data.min()

# To Find Mean Temperature
def Mean_Temp(Maximum_temp, Minimum_temp):
    return (Maximum_temp+Minimum_temp)/2

# For Users to give Planting and Harvesting date of crop
def User_Dates():
    Planting_date= convert_StringtoTimestamp(raw_input("Planting date of a crop: "))
    Harvesting_date= convert_StringtoTimestamp(raw_input("Harvesting date of a crop: "))
    
# To convert string into time format
def convert_StringtoTimestamp(string):
    return pd.to_datetime(string)

# For users to defined base temperature for a crop
def User_BaseTemp():
    return raw_input("Base temperature is ")


print "Weather data of kisanhub.csv file is: " 
print Reading_weatherfile

print "After calculating missing weather data using linear interpolation method, Corrected weather data is:  "
Corrected_WeatherFile= Finding_MissingWeatherData (Reading_weatherfile, "01/01/2014", "31/05/2016")
print Corrected_WeatherFile 

ResampleData=Resample_data(Corrected_WeatherFile)
#print ResampleData

print "Daily maximum temperature of given time series:  "
MaximumTemp= Maximum_Temp(ResampleData)
print MaximumTemp

print "Daily minimum temperature of given time series:  "
MinimumTemp= Minimum_Temp(ResampleData)
print MinimumTemp

print "Daily mean temperature of given time series:  "
MeanTemp=Mean_Temp(MaximumTemp, MinimumTemp)
print MeanTemp

Planting_Harvesting_date=User_Dates()

Base_Temperature= User_BaseTemp()


