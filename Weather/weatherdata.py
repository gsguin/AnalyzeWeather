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

class WeatherData():
    def __init__(self):
        self.name = 'WeatherData'
        self.pickleName = 'wd'
        self.parameterFile = 'data/parameter.csv'
        self.parameters = pd.read_csv(self.parameterFile, sep=',', header=0)
        self.stationHistoryData = self.__getStationHistoryData()
        #self.stationHistoryData = self.getStationHistoryData(self.getParameterValue('StationHistoryFilename')) #pd.read_csv(self.getParameterValue('StationHistoryFilename'), sep=',', skiprows=20)
        self.dataFormat = pd.read_csv(self.getParameterValue('DataFormat'), sep=',', header=0)
        self.truncateData() # to initialize the data with empty dataframe
#        columns=self.dataFormat.iloc[:,0].values.tolist()
#        columns.append(('FileName'))
#        self.data = pd.DataFrame(columns=columns)
        self.dataFileLocation = self.getParameterValue('DataLocation')
        #self.appendData(self.getParameterValue('SampleDataFile'))
        #self.data.truncate(before=1,after=0)
#        self.n_class = 2
#        self.datafile = 'data/titanic.csv'
#        self.train, self.test = self.load_data(self.datafile)
#        self.main3_attrs=[0,1,2]
#        self.main3_attr_labels=['PClass','Age','Sex']

    def getParameterValue(self, p_parameterName):
        # Returns the parameter value of a parameter
        # Parameters:
        #   p_parameterName : Name of the parameter specific to weather class (string)
        # Returns: string
        #
        df = self.parameters
        return df.loc[df['ParamName'] == p_parameterName].iat[0,df.columns.get_loc('ParamValue')]
                  
    def appendData(self, fileName):
        # Retrive the weather data from the file and append to the min dataset
        # Parameters:
        #   fileName : Name of the file to be loaded (string)
        # Returns: None
        # 
        temp_data = self.__readFixedWidthFile(p_structureData=self.dataFormat, p_fileName=fileName)
        temp_data['FileName'] = fileName[-20:][:12]
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
    
    def __getStationHistoryData(self):
        # Private method
        # Reads the StationHistoryData from the web file and returns the data
        # Parameters: None
        # Returns: dataframe
        structureData = pd.read_csv(self.getParameterValue('StationHistoryDataFormat'), sep=',', header=0)
        fileName = self.getParameterValue('StationHistoryFilename')
        skiprows = self.getParameterValue('StationHistoryFileHeaderRows')
        temp_data = self.__readFixedWidthFile(p_structureData=structureData, p_fileName=fileName, p_skiprows=skiprows)
        return temp_data
    
    def __readFixedWidthFile(self, p_structureData, p_fileName, p_skiprows=0, p_skipfooter=0):
        # Private method
        # Read data from a fixed-width text file based on the p_structuredata specification into a dataframe
        # Trim the data and change the data of numeric columns to numeric 
        # Parameters: 
        #   p_structureData : dataframe, with columns 'Field_Name', 'Start_Pos', 'Length', 'Data_Type'
        #   p_fileName : File name with full path (string)
        #   p_skiprows(oprional) : Number of rows (in int) need to be skipped at the beginning of file (including header row). Default value is 0.
        #   p_skipfooter(oprional) : Number of rows (in int) need to be skipped at the end of file. Default value is 0.
        # Returns: dataframe
        structure_data = p_structureData.sort_values(by=[p_structureData.columns[1]])   # sort by 2nd field, which is Starting position, in case it is not sorted 
        curr_position = 0
        flds = []
        for tmp_rec in structure_data.as_matrix(): # creating tuple with (start, end position) for each fields 
            start_pos = tmp_rec[1] - 1
            length = tmp_rec[2]
            if curr_position > start_pos:
                print('Data Fields ooverlap each other, correct the format spec')
            curr_position = start_pos + length
            flds.append((start_pos,curr_position))

        flds = tuple(flds)
        myParse = lambda line: tuple(line[i:j] for i, j in flds)
        
        raw_data = pd.read_csv(p_fileName, sep=',', skiprows=int(p_skiprows), skipfooter=int(p_skipfooter), header=None)
        
        final_data = raw_data.apply(lambda line: myParse(line[0]), axis=1) # applying the perser to cut each line on the specified locations which will later converted to columns
        columnNames = structure_data.iloc[:,0].values.tolist() # get the list of column names
        final_data = pd.DataFrame([list(i) for i in final_data], columns=columnNames) # convert series to list to store in dataframe
        final_data[final_data.columns] = final_data.apply(lambda x: x.str.strip()) # Strip the leading and trailing blanks
        numericColumns = structure_data[structure_data.iloc[:,3] == 'n'].iloc[:,0].values.tolist() # get the list of names of numerical columns
        final_data[numericColumns] = final_data[numericColumns].apply(pd.to_numeric, errors='ignore') # convert the data of numerical column to numeric
        return final_data

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
                    temp_data.append(hist_data[hist_data['USAF'] == t_USAF])
            hist_data = temp_data
        # similarly CTRY and ST filter can be added
        i=0
        fileNames = []
        for t_year in range(int(p_StartYear),int(p_EndtYear)):
            temp_data = hist_data[hist_data['BEGIN'] <= int(str(t_year)+'1231')]
            temp_data = temp_data[temp_data['END'] >= int(str(t_year)+'1231')]
            temp_data['Year'] = str(t_year)
            fileNames.extend((temp_data['Year'] + '/' + temp_data['USAF'] + '-' + temp_data['WBAN'] + '-' + temp_data['Year'] +'.gz').values.tolist())
        
        return fileNames
        

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
