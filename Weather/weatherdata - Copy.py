# -*- coding: utf-8 -*-
"""
Created on Wed Aug 15 09:48:59 2018

@author: GG9323
"""

#import csv
#import numpy as np
import sys
import pandas as pd
import struct
#import random
#import math

class WeatherData():
    def __init__(self):
        self.name = 'WeatherData'
        self.pickleName = 'wd'
        self.parameterFile = 'data/parameter.csv'
        self.parameters = pd.read_csv(self.parameterFile, sep=',', header=0)
        self.stationHistoryData = self.readFixedWidthFile()
        self.stationHistoryData = self.getStationHistoryData(self.getParameterValue('StationHistoryFilename')) #pd.read_csv(self.getParameterValue('StationHistoryFilename'), sep=',', skiprows=20)
        self.dataFormat = pd.read_csv(self.getParameterValue('DataFormat'), sep=',', header=None)
        self.data = 0
        self.appendData(self.getParameterValue('SampleDataFile'))
        self.data.truncate(before=1,after=0)
#        self.n_class = 2
#        self.datafile = 'data/titanic.csv'
#        self.train, self.test = self.load_data(self.datafile)
#        self.main3_attrs=[0,1,2]
#        self.main3_attr_labels=['PClass','Age','Sex']

    def getParameterValue(self, p_parameterName):
        df = self.parameters
        return df.loc[df['ParamName'] == p_parameterName].iat[0,df.columns.get_loc('ParamValue')]
                  
    def appendData(self, fname):
        col_specs = self.dataFormat.loc[:,1:2].values.tolist()
        col_names = self.dataFormat.loc[:,0].values.tolist()
        temp_data = pd.read_fwf(fname, colspecs=col_specs, header=None, names=col_names)
        if type(self.data) is int:
            self.data = temp_data
        else:
            self.data = self.data.append(temp_data)
        return
    
    def getStationHistoryData(self, fname):
        structure_data = pd.read_csv(self.getParameterValue('StationHistoryDataFormat'), sep=',', header=None)
        col_specs = [(0,7), (7,6), (13,31), (43,3), (48,3), (51,5), (57,8), (65,8), (74,8), (82,9), (91,8)] #structure_data.loc[:,1:2].values.tolist()
        col_names = structure_data.loc[:,0].values.tolist()
        temp_data = pd.read_fwf(fname, colspecs=col_specs, skiprows=20) #names=col_names, skiprows=22)
        return temp_data
    
    def readFixedWidthFile(self): #, p_structureData, p_fileName):
        structure_data = pd.read_csv(self.getParameterValue('StationHistoryDataFormat'), sep=',', header=0)
        #structure_data = p_structureData.sort_values(by=[p_structureData.columns[1]])   # sort by 2nd field, which is Starting position, in case it is not sorted 
        curr_position = 0
        #parse_format = ""
        fieldwidths = []
        flds = []
        flds1 = []
        for tmp_rec in structure_data.as_matrix():
            start_pos = tmp_rec[1] - 1
            length = tmp_rec[2]
            if curr_position < start_pos:
                fieldwidths.append(curr_position-start_pos)
                flds.append((False,curr_position,start_pos))
                curr_position = start_pos
            if curr_position > start_pos:
                print('Data Fields ooverlap each other, correct the format spec')
            fieldwidths.append(length)
            curr_position += length
            flds.append((True,start_pos,curr_position))
            flds1.append((start_pos,curr_position))

        flds = tuple(flds1)
#        cuts = tuple(cut for cut in accumulate(abs(fw) for fw in fieldwidths))
#        pads = tuple(fw < 0 for fw in fieldwidths) # bool values for padding fields
#        flds = tuple(izip_longest(pads, (0,)+cuts, cuts))[:-1]  # ignore final one
        #myParse = lambda line: tuple(line[i:j] for pad, i, j in flds if pad)
        myParse = lambda line: tuple(line[i:j] for i, j in flds)
        
        raw_data = pd.read_csv(self.getParameterValue('StationHistoryFilename'), sep=',', skiprows=22, header=None)
        
        final_data = raw_data.apply(lambda line: myParse(line[0]), axis=1)
        columnNames = [i for i in structure_data['Field_Name']]
        final_data = pd.DataFrame([list(i) for i in final_data], columns=columnNames)
        return final_data
    
    def readFixedWidthFile_o(self):
        structure_data = pd.read_csv(self.getParameterValue('StationHistoryDataFormat'), sep=',', header=0)
        structure_data = structure_data.sort_values(by=['Start_Pos'])
        curr_position = 0
        parse_format = ""
        for tmp_rec in structure_data.as_matrix():
            start_pos = tmp_rec[1] - 1
            length = tmp_rec[2]
            if start_pos > curr_position:
                parse_format += str(start_pos - curr_position) + "x "
            parse_format += str(length) + "s "
            curr_position = start_pos + length
        #field_indices = range(len(fieldspecs))
        #print curr_position, parse_format
        myParser = struct.Struct(parse_format).unpack_from
#        if sys.version_info[0] >= 3:
#            # converts unicode input to byte string and results back to unicode string
#            myParser = lambda line: tuple(s.decode() for s in myParser(line.encode()))
           
        raw_data = pd.read_csv(self.getParameterValue('StationHistoryFilename'), sep=',', skiprows=22, header=None)
        
        final_data = raw_data.apply(lambda line: myparser(line), axis=1)
        return final_data