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


df1 = df.iloc[:,[2,3,4,5,6,14,16,8,21,22,23,32,33,37]]

df2 = df1[df1['TransactionName'] == 'END']



#######################################
#########Data Cleaning
#######################################


df2 = df2.drop_duplicates()                                                                             ##Remove all duplicates


df2 = df2.drop_duplicates(subset = ['OrderNo','OperationNo','OperationName','ResourceGroup','ActualResource','ActualSetupStart','ActualEndTime','ActualStartTime']) 
#df2.drop_duplicates(subset = ['ActualResource','ActualSetupStart','ActualEndTime','ActualStartTime'])  ##Remove all duplicates if same resource group and all same start and end and setup time


df2 = df2.dropna(axis = 0, subset = ['OrderNo'])                                                        ##Drop NA values
df2 = df2.dropna(axis = 0 , how= 'all', subset = ['OperationNo','OperationName'])                       ##Drop NA values
df2 = df2.dropna(axis = 0 , how= 'all', subset = ['Product','PartNo'])                                  ##Drop NA values

Order = list(df2['OrderNo'].unique())


###############################################
#######Production Sequence and Unique Sequence
###############################################
seq_class = []
seq = pd.DataFrame({'dummy':np.arange(1,1000)})          ##list with actual sequence of machines for each order no.         
seq_1 = pd.DataFrame({'dummy':np.arange(1,1000)})

       ##list by removing machines with multiple use in sequence
for i in range(0,len(Order)):
    x = df2[df2['OrderNo'] == Order[i]]
    x = x.sort_values(by = ['OperationNo'], ascending = True)
    l = list(x['ResourceGroup'])
    z = pd.DataFrame(list(x['ResourceGroup']))
  
    if ((len(l)==1) and (l[0]=='MPC')):
        seq_class.append('Future')
    elif((len(l) > 1) and (l[0]=='MPC') and (l[len(l)-1]!= 'STK')):
        seq_class.append('In Process')
    elif ((len(l) > 2) and (l[0]=='MPC') and (l[len(l)-1]=='STK')):
        seq_class.append('Completed(MPC - STK)')
    elif((len(l) > 1) and (l[0]!='MPC') and (l[len(l)-1]== 'STK')):
        seq_class.append('Completed')
    else:
        seq_class.append('In Process')
        
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
seq1['combined'] = seq1[col].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)       ##########
                                                                                             
seq1['OrderNo'] = seq1.index
seq1['seq_class'] = seq_class
seq1.reset_index(inplace=True)
seq1 = seq1.drop('index',axis=1)
seq1['OrderNo'] = seq1['OrderNo'].astype(int)


df2.reset_index(inplace=True)
df2 = df2.drop('index',axis=1)
df2['OrderNo']=df2['OrderNo'].astype(int)


sequence = pd.DataFrame(seq1[['combined','OrderNo','seq_class']])

sequence = sequence.drop_duplicates(subset=['combined'])
sequence.reset_index(inplace=True)
sequence = sequence.drop('index',axis=1)
sequence.index += 1
sequence['No'] = list(range(1,sequence.shape[0]+1))


table1= pd.merge(sequence,df2,how = 'left',left_on = 'OrderNo', right_on = 'OrderNo')
table1.reset_index(inplace=True)
table1 = table1.drop('index',axis=1)
table1 = table1.sort_values(['OrderNo','OperationNo'], ascending = True)

#############################################
#############Table 2
#############################################


sequence1 = pd.DataFrame(seq1[['combined','OrderNo','seq_class']])
sequence1.reset_index(inplace=True)
sequence1 = sequence1.drop('index',axis=1)
sequence1.index += 1

table2 = pd.merge(sequence1,df2,how = 'left', left_on = 'OrderNo', right_on = 'OrderNo')
table2.reset_index(inplace=True)
table2 = table2.drop('index',axis=1)
table2 = table2.sort_values(['OrderNo','OperationNo'], ascending = True)


################################
##Creating CSV file
##############################
table1.to_csv('table1.csv')
table2.to_csv('table2.csv')

