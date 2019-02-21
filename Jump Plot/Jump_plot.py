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
df1 = df.iloc[:,[2,3,4,5,6,14,16,8,21,22,23,32,33,37]]

df2 = df1[df1['TransactionName'] == 'END']
df2.columns


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
seq_1 = pd.DataFrame({'dummy':np.arange(1,1000)})        ##list by removing machines with multiple use in sequence
for i in range(0,len(Order)):
    x = df2[df2['OrderNo'] == Order[i]]
    x = x.sort_values(by = ['OperationNo'], ascending = True)
    l = list(x['ResourceGroup'])
    z = pd.DataFrame(list(x['ResourceGroup']))
  
    if ((len(l)==1) and (l[0]=='MPC')):
        seq_class.append('future Sequences')
    elif((len(l) > 1) and (l[0]=='MPC') and (l[len(l)-1]!= 'STK')):
        seq_class.append('In Process')
    elif ((len(l) > 2) and (l[0]=='MPC') and (l[len(l)-1]=='STK')):
        seq_class.append('Completed_full')
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
seq1['combined'] = seq1[col].apply(lambda row: '_'.join(row.values.astype(str)), axis=1)
seq1['OrderNo'] = seq1.index
seq1['seq_class'] = seq_class
seq1.reset_index(inplace=True)
seq1 = seq1.drop('index',axis=1)
seq1['OrderNo'] = seq1['OrderNo'].astype(int)


seq1 = seq1[seq1['seq_class'] == 'Completed_full']
seq1.reset_index(inplace=True)
seq1 = seq1.drop('index',axis=1)


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

####################################
#################Creating CSV file
#####################################

table1.to_csv('table1.csv')
table2.to_csv('table2.csv')

######################################################################################
##########To find sequence with maximum order Number and with step count greater than 6
########################################################################################

combined_list = list(table2['combined'].unique())

table22 = table2[table2['combined']==combined_list[0]]    
    #jump = table2[table2['combined']==l[0]]
jump = table22.loc[:,['combined','OrderNo','OperationNo','Product','OperationName','ResourceGroup','ActualSetupStart','ActualEndTime']]
    
g= jump.groupby('OrderNo')


#table3 = pd.DataFrame(table2.groupby('combined').apply(lambda xx: xx.groupby('OrderNo').TotalQuantity.first().sum()).reset_index(name='correct_TotalQuantity'))    
    #jump1[['ActualSetupStart','ActualEndTime','OrderNo']].sort_values('OrderNo')
jump['ResourceGroup']    
'''
jump['event start #'] = jump['OperationNo']
jump['event end #'] = jump.groupby('OrderNo')['OperationNo'].shift(-1)
'''  
jump['event start #'] = g['OperationNo'].rank(ascending= True).astype(int)
jump['event end #'] = g['OperationNo'].rank(ascending= True).astype(int).shift(-1)


      
    
jump['event start name'] =  jump['ResourceGroup']
jump['event stop name'] = jump.groupby('OrderNo')['ResourceGroup'].shift(-1)
jump['start time'] = pd.to_datetime(jump['ActualEndTime'])
jump['stop time'] = pd.to_datetime(jump['ActualSetupStart'].shift(-1))
jump['total'] =(jump['stop time'] - jump['start time'])/np.timedelta64(1,'h')
    
jump.head()
jump.dropna(axis=0,how='any',inplace=True)    
jump.columns 
    #jump = jump[['combined','OrderNo','event start #','event end #','event start name','event stop name','total']]
jump['path'] =  jump.loc[:,['combined','OrderNo','event start #','event end #']].apply(lambda row: '.'.join(row.values.astype(str)), axis=1)

jump1 = jump.copy(deep=True)    
jump1.insert(jump1.shape[1]-1,'pathorder','1')
jump1['EventSeq#'] = jump1['event start #']
jump1['event type'] = jump1['event start name']
          
jump2 = jump.copy(deep=True)  
jump2.insert(jump2.shape[1]-1,'pathorder','2')
jump2['EventSeq#'] = jump2['event end #']
jump2['event type'] = jump2['event stop name']
jump = jump1.append(jump2,ignore_index=True)
jump = jump.sort_values(['EventSeq#','path','pathorder'])
jump.insert(jump.shape[1]-1,'rank',0)
jump[['event start #','event end #','EventSeq#']] = jump[['event start #','event end #','EventSeq#']].astype(int)
jump333 = jump.copy(deep=True)



for i in range(1,len(combined_list)):
    table23 = table2[table2['combined']==combined_list[i]]    
    #jump = table2[table2['combined']==l[0]]
    jump = table23.loc[:,['combined','OrderNo','OperationNo','Product','OperationName','ResourceGroup','ActualSetupStart','ActualEndTime']]
    g= jump.groupby('OrderNo')
    
    #jump1[['ActualSetupStart','ActualEndTime','OrderNo']].sort_values('OrderNo')
    
    jump['event start #'] = g['OperationNo'].rank(ascending= True)
    jump['event end #'] = g['OperationNo'].rank(ascending= True).astype(int).shift(-1)
        
    
    jump['event start name'] =  jump['ResourceGroup']
    jump['event stop name'] = jump.groupby('OrderNo')['ResourceGroup'].shift(-1)
    jump['start time'] = pd.to_datetime(jump['ActualEndTime'])
    jump['stop time'] = pd.to_datetime(jump['ActualSetupStart'].shift(-1))
    jump['total'] =(jump['stop time'] - jump['start time'])/np.timedelta64(1,'h')
    
    jump.dropna(axis=0,how='any',inplace=True)    

    #jump = jump[['combined','OrderNo','event start #','event end #','event start name','event stop name','total']]
    jump['path'] =  jump.loc[:,['combined','OrderNo','event start #','event end #']].apply(lambda row: '.'.join(row.values.astype(str)), axis=1)
    
    jump1 = jump.copy(deep=True)    
    jump1.insert(jump1.shape[1]-1,'pathorder','1')
    jump1['EventSeq#'] = jump1['event start #']
    jump1['event type'] = jump1['event start name']
          
    jump2 = jump.copy(deep=True)  
    jump2.insert(jump2.shape[1]-1,'pathorder','2')
    jump2['EventSeq#'] = jump2['event end #']
    jump2['event type'] = jump2['event stop name']
    
    jump = jump1.append(jump2,ignore_index=True)
    jump = jump.sort_values(['EventSeq#','path','pathorder'])
    jump.insert(jump.shape[1]-1,'rank',i)
    jump[['event start #','event end #','EventSeq#']] = jump[['event start #','event end #','EventSeq#']].astype(int)
    
    
    combined_list[i] = jump.copy(deep=True)
    jump333 = combined_list[i].append(jump333,ignore_index=True)    

    
jump333.to_csv('jump11.csv')