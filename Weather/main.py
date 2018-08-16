# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 12:08:50 2018

@author: GG9323
"""

import pandas as pd
from weatherdata import WeatherData as wd
from weatherstationdata import WeatherStationData as wsd
from utils import Utils as ut
import matplotlib.pyplot as plt


    
def main():
    q_parameterFile = 'data/query_parameter.csv'
    q_parameters = pd.read_csv(q_parameterFile, sep=',', header=0)
    
    curStartYear = ut.getParameterValue(q_parameters, 'StartYear')
    curEndYear = ut.getParameterValue(q_parameters, 'EndYear')
    curStartLat = ut.getParameterValue(q_parameters, 'StartLat')
    curEndLat = ut.getParameterValue(q_parameters, 'EndLat')
    curStartLon = ut.getParameterValue(q_parameters, 'StartLon')
    curEndLon = ut.getParameterValue(q_parameters, 'EndLon')
    curUSAFList = ut.getParameterValue(q_parameters, 'USAFList')
    curCTRYList = ut.getParameterValue(q_parameters, 'CTRYList')
    curSTList = ut.getParameterValue(q_parameters, 'STList')
    weatherData = wd()
    weatherStationData = wsd()
    #print (weatherData.data)
    fileNames = weatherStationData.getFilenames(p_StartYear=curStartYear, p_EndtYear=curEndYear, p_USAFList=curUSAFList, p_CTRYList=curCTRYList, p_STList=curSTList)
    for t_filename in fileNames:
        weatherData.appendData(weatherData.dataFileLocation+t_filename)
    
    
    #print(weatherData.data.head)
    myData = weatherData.data.infer_objects()
    #myData = weatherData.data
    myData[myData['Air Temperature'] == -9999] = None
    tmpData = myData.groupby(['FileName', 'Observation Month'])['Air Temperature'].mean()
    
    print(tmpData)
    myData[['Observation Month','Air Temperature']].plot(x='Observation Month',y='Air Temperature', kind='scatter')
    myData[['Observation Month','Air Temperature']].boxplot(column='Air Temperature', by='Observation Month')
    
    
if __name__ == "__main__":
    main()

