import pandas as pd
import csv
import datetime
import matplotlib.pyplot as plt


class WeatherdataFromFile:
    def reading_weather_dataframe(self):
        return pd.read_csv ("kisanhub.csv",index_col=['record_ts'],parse_dates=True)

class MissingDataFinder:
    def __init__(self,weather_dataframe):
        self.weather_dataframe= weather_dataframe
    def get_missingvalue_of_dataframe(self):
        # it gives date range from starting date to final date with hourly frequency
        daterange= pd.date_range( self.weather_dataframe.index[0],self.weather_dataframe.index[-1] ,freq='H')
        # reindex the whole dataframe by placing "NaN" in locations having no value in the previous index.
        reindex_weather_dataframe= self.weather_dataframe.reindex(daterange, fill_value="Nan")
        # convert datatype of dataframe to float
        convert_datatype=reindex_weather_dataframe.astype(float)
        # calculate missing values where "Nan" is located, using linear interpolation method
        corrected_weather_dataframe= convert_datatype.interpolate(method='linear')
        return corrected_weather_dataframe
        
class MeanCalculator:
    def __init__(self,dataframe):
        self.dataframe= dataframe
    def get_resample_dataframe(self):
        return self.dataframe.resample('24H')
    def get_max_value_dataframe(self,resample_dataframe):
        self.resample_dataframe= resample_dataframe
        return self.resample_dataframe.max()
    def get_min_value_dataframe(self,resample_dataframe):
        self.resample_dataframe= resample_dataframe
        return self.resample_dataframe.min()
    def get_mean_value_dataframe(self,max_value_dataframe,min_value_dataframe):
        return (max_value_dataframe+min_value_dataframe)/2
    
class UserInputs:
    def input_planting_date(self):
        print "Planting Date of crop is : "
        try:
        # if planting date is in correct format, it convert string of planting date to datetime format 
            return datetime.date(int(raw_input("Year: ")),int(raw_input("Month: ")),int(raw_input("Day: ")))
        except ValueError:
        # if planting date is not in format, give error message with one more chance to input planting date
            print "Error: Please follow Year-Month-Day in integer format. Try again"
            planting_date= input_of_user.input_planting_date()
    def input_harvesting_date(self):
        print "Harvesting Date of crop is : "
        try:
        # if harvesting date is in correct format, it convert string of harvesting date to datetime format
            return datetime.date(int(raw_input("Year: ")),int(raw_input("Month: ")),int(raw_input("Day: ")))
        except ValueError:
        # if harvesting date is not in format, give error message with one more chance to input harvesting date
            print"Error: Please follow Year-Month-Day in integer format. Try again"
            harvesting_date= input_of_user.input_harvesting_date()
    def input_base_temp(self):
        # For users to defined base temperature for a crop
        try:
        # if base temperature is number, then it convert number to float
            return float(raw_input("Base temperature is "))
        except ValueError:
        # if base temperature is not number, then give error with chance to input base temperature 
            print "Error: Please give numbers only"
            base_temp= input_of_user.input_base_temp()
            
class GrowingDegreeDaysCalculator:
     def __init__(self,base_temp,meantemp,planting_date,harvesting_date):
        self.base_temp= base_temp
        self.meantemp= meantemp
        self.planting_date= planting_date
        self.harvesting_date= harvesting_date
     
     def get_growing_degree_days(self):
        growing_duration= pd.date_range(self.planting_date,self.harvesting_date,freq='D')
        # reindex meantemperature for crop growth duration, reindex function used
        growingtime_meantemp= self.meantemp.reindex(growing_duration)
        # if mean temp is lower than base temp, replace it with base temp, because crop can not grow below base temp.
        growingtime_meantemp.value=growingtime_meantemp.value.where(growingtime_meantemp.value>= self.base_temp)
        growingtime_meantemp['value']=growingtime_meantemp['value'].replace(['NaN'], self.base_temp)
        # to calculate each days contribution to GDD
        eachday_gdd_contribution=growingtime_meantemp-self.base_temp
        # for a particular crop growing degree days is
        growing_degree_days= eachday_gdd_contribution.cumsum()
        return growing_degree_days
    
    
class GddTimeGraphPlotter:
    def __init__(self,growing_degree_days):
        self.growing_degree_days= growing_degree_days
    def plot_gdd_graph(self):
    # plot graph of growing degree days with respect to time
        self.growing_degree_days.plot.line(y='value', use_index=True, title='Growing degree days')
        plt.show()
        
        
weather_dataframe=WeatherdataFromFile().reading_weather_dataframe()         
corrected_weather_dataframe= MissingDataFinder(weather_dataframe).get_missingvalue_of_dataframe()
temperature_dataframe= MeanCalculator(corrected_weather_dataframe)
resampled_temp_dataframe= temperature_dataframe.get_resample_dataframe()
max_temp_dataframe= temperature_dataframe.get_max_value_dataframe(resampled_temp_dataframe)
min_temp_dataframe= temperature_dataframe.get_min_value_dataframe(resampled_temp_dataframe)
mean_temp_dataframe= temperature_dataframe.get_mean_value_dataframe(max_temp_dataframe,min_temp_dataframe)
user_input_object=UserInputs()
planting_date= user_input_object.input_planting_date()
harvesting_date= user_input_object.input_harvesting_date()
base_temp= user_input_object.input_base_temp()
gdd_calculator_object=GrowingDegreeDaysCalculator(base_temp,mean_value_dataframe,planting_date,harvesting_date)
growing_degree_days=gdd_calculator_object.get_growing_degree_days()
gdd_graph_object= GddTimeGraphPlotter(growing_degree_days)
print (gdd_graph_object.plot_gdd_graph())

