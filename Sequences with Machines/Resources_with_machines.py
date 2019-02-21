# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 08:56:04 2018

@author: u4ac_kpa
"""

####################################################################
####Import Libraries
#####################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os        
import seaborn as sns
import math
import xlrd
from textwrap import wrap
#from matplotlib.ticker import MultipleLocator, FormatStrFormatter
import matplotlib.ticker as ticker


##########################################################################
#####Import Excel files
#########################################################################

df = pd.read_csv('FV_data_dump.csv')

df = df.drop_duplicates()

df = df.drop_duplicates()
df1 = df.iloc[:,[2,3,4,5,6,16,8,21,22,23,32,33,37]]

df2 = df1[df1['TransactionName'] == 'END']



#######################################
#########Data Cleaning
#######################################


df2 = df2.drop_duplicates()                                                                                ##Remove all duplicates


df2 = df2.drop_duplicates(subset = ['OrderNo','OperationNo','OperationName','ActualResource','ActualSetupStart','ActualEndTime','ActualStartTime']) 
#df2.drop_duplicates(subset = ['ActualResource','ActualSetupStart','ActualEndTime','ActualStartTime'])      ##Remove all duplicates if same resource group and all same start and end and setup time


df2 = df2.dropna(axis = 0, subset = ['OrderNo'])                                                            ##Drop NA values
df2 = df2.dropna(axis = 0 , how= 'all', subset = ['OperationNo','OperationName'])                           ##Drop NA values
df2 = df2.dropna(axis = 0 , how= 'all', subset = ['Product','PartNo'])                                      ##Drop NA values

Order = list(df2['OrderNo'].unique())


###############################################
########Production Sequence and Unique Sequence
###############################################

seq = pd.DataFrame({'dummy':np.arange(1,1000)})             ##list with actual sequence of machines for each order no.         
seq_1 = pd.DataFrame({'dummy':np.arange(1,1000)})           ##list by removing machines with multiple use in sequence
for i in range(0,len(Order)):
    x = df2[df2['OrderNo'] == Order[i]]
    x = x.sort_values(by = ['OperationNo'], ascending = True)
    
    z = pd.DataFrame(list(x['ActualResource']))
    
    seq['%s'%(Order[i])] = z[0]
    
######Sequence with all machines for each order#

seq = seq.drop('dummy', axis = 1)
seq = seq.dropna(axis = 0, how = 'all') 
seq = seq.dropna(axis = 1, how = 'all')
seq.index += 1
seq1 = seq.T

######################################################################
#With unique sequence no. of orders, total quantity and total product
######################################################################


seq1.iloc[:,0]
col = list(seq1.columns)
seq1['combined'] = seq1[col].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
seq1['OrderNo'] = seq1.index
seq1.reset_index(inplace=True)
seq1 = seq1.drop('index',axis=1)
seq1['OrderNo'] = seq1['OrderNo'].astype(int)
seq1.dtypes

'''
df3 = df2.iloc[:,[0,3,6]]
df3.reset_index(inplace= True)
df3 = df3.drop('index',axis=1)
df3.reset_index(inplace=True)
df3 = df3.drop('index',axis=1)
df3['OrderNo']=df3['OrderNo'].astype(int)
df3.dtypes
df2.columns
'''

df2.reset_index(inplace=True)
df2 = df2.drop('index',axis=1)
df2['OrderNo']=df2['OrderNo'].astype(int)
df2.shape

sequence = pd.DataFrame(seq1[['combined','OrderNo']])
sequence = sequence.drop_duplicates(subset=['combined'])
sequence.reset_index(inplace=True)
sequence = sequence.drop('index',axis=1)
sequence.index += 1
sequence['No'] = list(range(1,sequence.shape[0]+1))

sequence.columns
sequence.shape


table1 = pd.merge(sequence,df2,how = 'left',left_on = 'OrderNo', right_on = 'OrderNo')
table1.reset_index(inplace=True)
table1 = table1.drop('index',axis=1)
table1 = table1.sort_values(['OrderNo','OperationNo'], ascending = True)
table1.columns
table1.shape
######################
###Table 2


sequence1 = pd.DataFrame(seq1[['combined','OrderNo']])

sequence1.reset_index(inplace=True)
sequence1 = sequence1.drop('index',axis=1)
sequence1.index += 1


sequence.columns
sequence.shape


table2 = pd.merge(sequence1,df2,how = 'left',left_on = 'OrderNo', right_on = 'OrderNo')
table2.reset_index(inplace=True)
table2 = table2.drop('index',axis=1)
table2 = table2.sort_values(['OrderNo','OperationNo'], ascending = True)
table2.shape
df2.shape


writer = pd.ExcelWriter('table1.xlsx', engine='xlsxwriter')
# Write your DataFrame to a file     
table1.to_excel(writer, 'Sequence')
#VLT1.to_excel(writer,'VLT1')   
writer.save() 


writer = pd.ExcelWriter('table2.xlsx', engine='xlsxwriter')
# Write your DataFrame to a file     
table2.to_excel(writer, 'table2')
#VLT1.to_excel(writer,'VLT1')   
writer.save() 




























'''





df555 = pd.DataFrame(table.groupby('combined').size().sort_values(ascending = False))
df555['Unique Part No'] = table.groupby('combined')['PartNo'].nunique().sort_values()
df555['Unique Order No'] = table.groupby('combined')['OrderNo'].nunique().sort_values()

df555['Total Quantity'] = table.groupby('combined')['TotalQuantity'].sum()
df555 = df555.drop([0],axis = 1)
df555 = df555.reset_index()
df555['combined'] = df555['combined'].astype(str)


seq2 = seq1.drop_duplicates(['combined'])
df66 = pd.merge(df555,seq2,how='left',left_on = 'combined',right_on='combined')
df66 = df66.drop(['OrderNo','combined'],axis=1)


###Sequence with unique machines
seq_1 = seq_1.drop('dummy', axis = 1)
seq_1 = seq_1.dropna(axis = 0, how = 'all') 
seq_1 = seq_1.dropna(axis = 1, how = 'all')
seq_1.index += 1
seq1 = seq_1.T


seq1.iloc[:,0]
col = list(seq1.columns)
seq1['combined'] = seq1[col].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
seq1['OrderNo'] = seq1.index
seq1.reset_index(inplace=True)
seq1 = seq1.drop('index',axis=1)
seq1['OrderNo'] = seq1['OrderNo'].astype(int)

seq1.dtypes


df3 = df2.iloc[:,[0,3,6]]
df3.reset_index(inplace= True)
df3 = df3.drop('index',axis=1)
df3.reset_index(inplace=True)
df3 = df3.drop('index',axis=1)
df3['OrderNo']=df3['OrderNo'].astype(int)
df3.dtypes


table= pd.merge(seq1,df3,how = 'left',left_on = 'OrderNo', right_on = 'OrderNo')
table.reset_index(inplace=True)
table = table.drop('index',axis=1)





df555 = pd.DataFrame(table.groupby('combined').size().sort_values(ascending = False))
df555['Unique Part No'] = table.groupby('combined')['PartNo'].nunique().sort_values()
df555['Unique Order No'] = table.groupby('combined')['OrderNo'].nunique().sort_values()

df555['Total Quantity'] = table.groupby('combined')['TotalQuantity'].sum()
df555 = df555.drop([0],axis = 1)
df555 = df555.reset_index()
df555['combined'] = df555['combined'].astype(str)

seq2=seq1.drop_duplicates(['combined'])
df55 = pd.merge(df555,seq2,how='left',left_on = 'combined',right_on='combined')
df55 =df55.drop(['OrderNo','combined'],axis=1)

#############################

uniq_seq = seq1.drop_duplicates()
unique_seq = uniq_seq.reset_index()
unique_seq.index += 1
unique_seq = unique_seq.drop(['index'],axis=1)

#################################################
###############Ressource Utilization
##################################################

df333 = pd.DataFrame(df2.groupby('ActualResource').size().sort_values(ascending = False))
df333['Total Unique Product'] = df2.groupby('ActualResource')['Product'].nunique()
df333['Total Unique Order'] = df2.groupby('ActualResource')['OrderNo'].nunique()
df333['Total Order'] = df2.groupby('ActualResource')['OrderNo'].size()
df333['Total Quantity'] = df2.groupby('ActualResource')['TotalQuantity'].sum()
df333['Total Operation Time Seconds'] = df2.groupby('ActualResource')['ActualOperationTimeSeconds'].sum()
df333['Total Operation Time Hour'] = df333['Total Operation Time Seconds']/3600
df333['Total Operation Time Hour'] = df333['Total Operation Time Hour'].round(1) 
df333['Total Setup Time Seconds'] = df2.groupby('ActualResource')['ActualSetupTimeSeconds'].sum()
df333['Total Setup Time Hour'] = df333['Total Setup Time Seconds']/3600
df333['Total Setup Time Hour'] = df333['Total Setup Time Hour'].round(1) 
df333['Total Utilization Time (Hour)'] = df333['Total Setup Time Hour'] + df333['Total Operation Time Hour'] 
df333 = df333.drop([0],axis = 1)

#############################
####Excel Writer
#############################

writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
# Write your DataFrame to a file     
seq1.to_excel(writer, 'Sequence')
unique_seq.to_excel(writer, 'Unique_Sequence')
df333.to_excel(writer, 'Resource_Utilization')
df55.to_excel(writer,'sequence_without_duplicates')
df66.to_excel(writer,'sequence_with_duplicates')
#VLT1.to_excel(writer,'VLT1')   
writer.save() 


'''








































































































































































































































































































































