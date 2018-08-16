# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 09:48:59 2018

@author: GG9323
"""

#import csv
#import numpy as np
#import sys
import pandas as pd
#import struct
#import random
#import math
from utils import Utils as ut


class WeatherData():
    def __init__(self):
        self.name = 'WeatherData'
        self.pickleName = 'wd'
        self.parameterFile = 'data/parameter.csv'
        self.parameters = pd.read_csv(self.parameterFile, sep=',', header=0)
        self.dataFormat = pd.read_csv(self.getParameterValue('DataFormat'), sep=',', header=0)
        self.truncateData() # to initialize the data with empty dataframe
        self.dataFileLocation = self.getParameterValue('DataLocation')

    def getParameterValue(self, p_parameterName):
        # Returns the parameter value of a parameter
        # Parameters:
        #   p_parameterName : Name of the parameter specific to weather class (string)
        # Returns: string
        #
        df = self.parameters
        return df.loc[df['ParamName'] == p_parameterName].iat[0,df.columns.get_loc('ParamValue')]
                  
    def appendData(self, p_fileName):
        # Retrive the weather data from the file and append to the min dataset
        # Parameters:
        #   p_fileName : Name of the file to be loaded (string)
        # Returns: None
        # 
        temp_data = ut.readFixedWidthFile(p_structureData=self.dataFormat, p_fileName=p_fileName)
        temp_data['FileName'] = p_fileName[-20:][:12]
        temp_data = self.cleanUpData(temp_data)
        if isinstance(self.data, pd.DataFrame):
            self.data = self.data.append(temp_data)
        else:
            self.data = temp_data
        return

    def truncateData(self):
        # Truncate the weather data of the object
        # Parameters: None
        # Returns: None
        # 
        columns=self.dataFormat.iloc[:,0].values.tolist()
        columns.append(('FileName'))
        self.data = pd.DataFrame(columns=columns)
        return
    
    def cleanUpData(self, p_data):
        # Cleans the data and returns the cleaned data
        # Parameters:
        #   p_data : Name of the file to be loaded (string)
        # Returns: DataFrame
        # *** Need to implement
        return p_data

def main():
    weatherData = WeatherData()
    #print (weatherData.data)
    curStartYear = weatherData.getParameterValue('StartYear')
    curEndYear = weatherData.getParameterValue('EndYear')
    curStartLat = weatherData.getParameterValue('StartLat')
    curEndLat = weatherData.getParameterValue('EndLat')
    curStartLon = weatherData.getParameterValue('StartLon')
    curEndLon = weatherData.getParameterValue('EndLon')
    curUSAFList = weatherData.getParameterValue('USAFList')
    curCTRYList = weatherData.getParameterValue('CTRYList')
    curSTList = weatherData.getParameterValue('STList')
    fileNames = weatherData.getFilenames(p_StartYear=curStartYear, p_EndtYear=curEndYear, p_USAFList=curUSAFList, p_CTRYList=curCTRYList, p_STList=curSTList)
    for t_filename in fileNames:
        weatherData.appendData(weatherData.dataFileLocation+t_filename)
    
    
    print(weatherData.data.head)
    
if __name__ == "__main__":
    main()
