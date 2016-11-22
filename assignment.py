import pandas as pd
import csv

# Reading weather dataframe of .csv format
def reading_weather_dataframe():
    return pd.read_csv ("kisanhub.csv",index_col=['record_ts'],parse_dates=True)

# To find missing values using Linear Interpolation method
def finding_missing_data (weather_dataframe, starting_date, final_date):
    # convert  string of starting date to datetime format 
    starting_date= convert_stringto_datetime(starting_date)
    print type(starting_date)
    print starting_date
    # convert  string of final date to datetime format 
    final_date= convert_stringto_datetime(final_date)
    print type(final_date)
    print final_date
    # it gives date range from starting date to final date with hourly frequency
    daterange= pd.date_range(starting_date, final_date,freq='H')
    print type(daterange)
    # reindex the whole dataframe by placing "NaN" in locations having no value in the previous index.
    reindex_weather_dataframe= weather_dataframe.reindex(daterange, fill_value="Nan")
    print type( reindex_weather_dataframe)
    # convert datatype of dataframe to float
    convert_datatype=reindex_weather_dataframe.astype(float)
    print type( convert_datatype)
    print convert_datatype
    # calculate missing values where "Nan" is located, using linear interpolation method
    corrected_weather_dataframe=convert_datatype.interpolate(method='linear')
    return corrected_weather_dataframe
    print type( corrected_weather_dataframe)
    # get corrected weathere dataframe 
    
    
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
    print "Planting Date of crop is : "
    try:
        # if planting date is in correct format, it convert string of planting date to datetime format 
        return datetime.date(int(raw_input("Year: ")),int(raw_input("Month: ")),int(raw_input("Day: ")))
    except ValueError:
        # if planting date is not in format, give error message with one more chance to input planting date
        print "Error: Please follow Year-Month-Day in integer format. Try again"
        planting_date= user_planting_date()

def user_harvesting_date():
    print "Harvesting Date of crop is : "
    try:
        # if harvesting date is in correct format, it convert string of harvesting date to datetime format
        return datetime.date(int(raw_input("Year: ")),int(raw_input("Month: ")),int(raw_input("Day: ")))
    except ValueError:
         # if harvesting date is not in format, give error message with one more chance to input harvesting date
        print"Error: Please follow Year-Month-Day in integer format. Try again"
        harvesting_date= user_harvesting_date()

# To convert string into time format
def convert_stringto_datetime(string):
    return pd.to_datetime(string)

# For users to defined base temperature for a crop
def user_base_temp():
    try:
        # if base temperature is number, then it convert number to float
        return float(raw_input("Base temperature is "))
    except ValueError:
        # if base temperature is not number, then give error with chance to input base temperature 
        print "Error: Please give numbers only"
        base_Temp= user_base_temp()

# to calculate growth duration of crop using growth_durationof_crop function
def growth_durationof_crop(planting_date, harvesting_date,freq='D'):
    return pd.date_range(planting_date, harvesting_date,freq='D')

# to calculate growing_degree_days
def growing_degree_days(base_temp, meantemp,planting_date, harvesting_date,freq='D'):
    # to calculate growth duration of crop growth_durationof_crop function used
    growing_duration= growth_durationof_crop(planting_date, harvesting_date,freq='D')
    print growing_duration
    print type(growing_duration)
    # reindex meantemperature for crop growth duration, reindex function used
    growingtime_meantemp= meantemp.reindex(growing_duration)
    # if mean temp is lower than base temp, replace it with base temp, because crop can not grow below base temp.
    growingtime_meantemp.value=growingtime_meantemp.value.where(growingtime_meantemp.value>= base_temp)
    print "mean temperature in growing duration of crop is: "
    print growingtime_meantemp
    print growingtime_meantemp.dtypes
    print type(growingtime_meantemp)
    growingtime_meantemp['value']=growingtime_meantemp['value'].replace(['NaN'], base_temp)
    print growingtime_meantemp
    # to calculate each days contribution to GDD
    eachday_gdd_contribution=growingtime_meantemp-base_temp
    print "each day contribution to growing degree days is: "
    print eachday_gdd_contribution
    print type(eachday_gdd_contribution)
    print eachday_gdd_contribution.dtypes
    # for a particular crop growing degree days is
    growing_degree_days= eachday_gdd_contribution.cumsum()
    print growing_degree_days
    print type(growing_degree_days)
    print growing_degree_days.dtypes
    print "growing degree days is "
    print growing_degree_days.tail(1)


# first read kisanhub.csv weather file using reading_weather_dataframe function and print weather dataframe
print "Weather data of kisanhub.csv file is: " 
weather_dataframe= reading_weather_dataframe ()
print weather_dataframe
print weather_dataframe.dtypes
print type(weather_dataframe)

print "After calculating missing weather data using linear interpolation method, Corrected weather data is:  "
# calculate missing weather data using finding_missing_data function and print corrected weather dataframe
corrected_weather_dataframe= finding_missing_data (weather_dataframe, "01/01/2014", "31/05/2016")
print corrected_weather_dataframe 
print corrected_weather_dataframe.dtypes
print type( corrected_weather_dataframe)

# to get daily dataframe from hourly weather dataframe resampling done using resample_dataframe function
resample_data= resample_dataframe( corrected_weather_dataframe)
print resample_data
print type( resample_data)

print "Daily maximum temperature of given time series:  "
# to get daily maximum temperature of given datetime series maximum_temp function used
max_temp=  maximum_temp(resample_data)
print max_temp
print max_temp.dtypes
print type( max_temp)

print "Daily minimum temperature of given time series:  "
# daily minimum temperature get using minimum_temp function
min_temp= minimum_temp(resample_data)
print min_temp
print min_temp.dtypes
print type(min_temp)

print "Daily mean temperature of given time series:  "
# to get daily mean temperature of given datetime series mean_temp function used
meantemp=mean_temp(max_temp, min_temp)
print meantemp
print meantemp.index
#print meantemp['20140102':'20140104']
#print meantemp[:1]
print meantemp.dtypes
print type(meantemp)

# user can input planting date and convert it in correct datetime format using user_planting_date function
planting_date= user_planting_date()
print planting_date
print type (planting_date)
# user can input harvesting date and convert it in correct datetime format using user_harvesting_date function
harvesting_date= user_harvesting_date()
print harvesting_date
print type( harvesting_date)

# user can input base temperature using user_base_temp function
base_temp= user_base_temp()
print base_temp
print type(base_temp)

growing_degree_days= growing_degree_days(base_temp, meantemp,planting_date, harvesting_date,freq='D')


