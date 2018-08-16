# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 07:43:57 2018

@author: GG9323
"""
import pandas as pd
from utils import Utils as ut

class WeatherStationData():
    def __init__(self):
        self.name = 'WeatherStationData'
        self.pickleName = 'wsd'
        self.parameterFile = 'data/parameter.csv'
        self.parameters = pd.read_csv(self.parameterFile, sep=',', header=0)
        self.stationHistoryData = self.__getStationHistoryData()

    def getParameterValue(self, p_parameterName):
        # Returns the parameter value of a parameter
        # Parameters:
        #   p_parameterName : Name of the parameter specific to weather class (string)
        # Returns: string
        #
        df = self.parameters
        return df.loc[df['ParamName'] == p_parameterName].iat[0,df.columns.get_loc('ParamValue')]
                  
    def __getStationHistoryData(self):
        # Private method
        # Reads the StationHistoryData from the web file and returns the data
        # Parameters: None
        # Returns: dataframe
        structureData = pd.read_csv(self.getParameterValue('StationHistoryDataFormat'), sep=',', header=0)
        fileName = self.getParameterValue('StationHistoryFilename')
        skiprows = self.getParameterValue('StationHistoryFileHeaderRows')
        temp_data = ut.readFixedWidthFile(p_structureData=structureData, p_fileName=fileName, p_skiprows=skiprows)
        return temp_data

    def getFilenames(self, p_StartYear, p_EndtYear, p_USAFList=None, p_CTRYList=None, p_STList=None):
        # Get the list of filenames which matches the given criteria.
        # If value of p_USAFList, p_CTRYList, p_STList is available, those are joined with AND operation.
        # p_StartYear, p_EndtYear values are also applied with AND condition.
        # Parameters: 
        #   p_USAFList(optional) : List of USAF values (list of string)
        #   p_CTRYList(optional) : List of CTRY values (list of string)
        #   p_STList(optional) : List of ST values (list of string)
        #   p_StartYear : Start of the year range (string)
        #   p_EndtYear : End of the year range (string)
        # Returns: list of filenames
        #
        
        hist_data = self.stationHistoryData
        if p_USAFList!='':
            #temp_data = temp_data[temp_data['USAF'] in p_USAFList.split(',')]
            i=0
            for t_USAF in p_USAFList.split(','):
                if i == 0 :
                    temp_data = hist_data[hist_data['USAF'] == t_USAF.strip()]
                    i += 1
                else:
                    temp_data = temp_data.append(hist_data[hist_data['USAF'] == t_USAF.strip()])
            hist_data = temp_data
        # similarly CTRY and ST filter can be added
        i=0
        fileNames = []
        for t_year in range(int(p_StartYear),int(p_EndtYear)+1):
            temp_data = hist_data[hist_data['BEGIN'] <= int(str(t_year)+'1231')]
            temp_data = temp_data[temp_data['END'] >= int(str(t_year)+'1231')]
            temp_data['Year'] = str(t_year)
            fileNames.extend((temp_data['Year'] + '/' + temp_data['USAF'] + '-' + temp_data['WBAN'] + '-' + temp_data['Year'] +'.gz').values.tolist())
        
        return fileNames
        
