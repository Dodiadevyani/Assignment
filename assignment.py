import pandas as pd
import csv

# Reading weather file of .csv format
def reading_weather_dataframe():
    return pd.read_csv ("kisanhub.csv",index_col=['record_ts'],parse_dates=True)

# To find missing values using Linear Interpolation method
def finding_missing_data (weather_dataframe, starting_date, final_date):
    starting_date= convert_stringto_datetime(starting_date)
    print type(starting_date)
    print starting_date
    final_date= convert_stringto_datetime(final_date)
    print type(final_date)
    print final_date
    daterange= pd.date_range(starting_date, final_date,freq='H')
    print type(daterange)
    reindex_weather_dataframe= weather_dataframe.reindex(daterange, fill_value="Nan")
    print type( reindex_weather_dataframe)
    convert_datatype=reindex_weather_dataframe.astype(float)
    print type( convert_datatype)
    print convert_datatype
    corrected_weather_dataframe=convert_datatype.interpolate(method='linear')
    return corrected_weather_dataframe
    print type( corrected_weather_dataframe)
 
# To resample data sets in 24hours group
def resample_dataframe(dataframe):
    return dataframe.resample('24H')

# To find Maximum Temperature
def maximum_temp(temp):
    return temp.max()

# To find Minimum Temperature
def minimum_temp(temp):
    return temp.min()

# To Find Mean Temperature
def mean_temp(maximum_temp, minimum_temp):
    return (maximum_temp+minimum_temp)/2

# For Users to give Planting and Harvesting date of crop
def user_planting_date():
    try:
        return convert_stringto_datetime(raw_input("Planting date of a crop: "))
    except ValueError:
        print "Please follow dd/mm/year or year/mm/dd format"
        planting_date= user_planting_date()

def user_harvesting_date():
    try:
        return convert_stringto_datetime(raw_input("Harvesting date of a crop: "))
    except ValueError:
        print "Please follow dd/mm/year or year/mm/dd format"
        harvesting_date= user_harvesting_date()

# To convert string into time format
def convert_stringto_datetime(string):
    return pd.to_datetime(string)

# For users to defined base temperature for a crop
def user_base_temp():
    try:
         return float(raw_input("Base temperature is "))
    except ValueError:
        print "Please give numbers only"
        base_Temp= user_base_temp()
        




print "Weather data of kisanhub.csv file is: " 
weather_dataframe= reading_weather_dataframe ()
print weather_dataframe
print weather_dataframe.dtypes
print type(weather_dataframe)

print "After calculating missing weather data using linear interpolation method, Corrected weather data is:  "

corrected_weather_dataframe= finding_missing_data (weather_dataframe, "01/01/2014", "31/05/2016")
print corrected_weather_dataframe 
print corrected_weather_dataframe.dtypes
print type( corrected_weather_dataframe)

resample_data= resample_dataframe( corrected_weather_dataframe)
print resample_data
print type( resample_data)

print "Daily maximum temperature of given time series:  "

max_temp=  maximum_temp(resample_data)
print max_temp
print max_temp.dtypes
print type( max_temp)

print "Daily minimum temperature of given time series:  "

min_temp= minimum_temp(resample_data)
print min_temp
print min_temp.dtypes
print type(min_temp)

print "Daily mean temperature of given time series:  "

meantemp=mean_temp(max_temp, min_temp)
print meantemp
print meantemp.dtypes
print type(meantemp)

planting_date= user_planting_date()
print planting_date
print type(planting_date)
harvesting_date= user_harvesting_date()
print harvesting_date
print type(harvesting_date)
base_temp= user_base_temp()
print base_temp
print type(base_temp)


