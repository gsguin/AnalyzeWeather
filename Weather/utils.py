# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 07:48:36 2018

@author: GG9323
"""
import pandas as pd

class Utils():
    def __init__(self):
        self.name = 'Utils'
        self.pickleName = 'ut'
 

    
    def readFixedWidthFile(p_structureData, p_fileName, p_skiprows=0, p_skipfooter=0):
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
        final_data = final_data.infer_objects() # change the column datatype acording to the data value
        return final_data

    def getParameterValue(p_parameters, p_parameterName):
        # Returns the parameter value of a parameter
        # Parameters:
        #   p_parameterName : Name of the parameter specific to weather class (string)
        # Returns: string
        #
        df = p_parameters
        return df.loc[df['ParamName'] == p_parameterName].iat[0,df.columns.get_loc('ParamValue')]