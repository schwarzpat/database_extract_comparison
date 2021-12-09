import glob
import os
import numpy as np
import pandas as pd
from xlsxwriter.workbook import Workbook

## this script assumes that the script assaumes table content extracted into csv files in the respective folders

db1_files = os.listdir('C:/Users/User/DB1 Folder/')
db1_list = [f for f in db1_files if f[-3:] == 'csv']

db2_files = os.listdir('C:/Users/User/DB2 Folder/')
db2_list = [f for f in db2_files if f[-3:] == 'csv']

db1_list_as_set = set(db1_list)
intersection = db1_list_as_set.intersection(db2_list)
intersection_as_list = list(intersection)
intersection_as_list.sort()
final_list = pd.DataFrame(intersection_as_list)

total_delta = pd.DataFrame()
writer = pd.ExcelWriter('C:/Users/User/Outout/output.xslx', engine='xlsxwriter')
workbook = writer.book

for table in intersection_as_list:
    db1 = pd.read_csv('C:/Users/User/DB1 Folder' + table, index_col=None, encoding='latin')
    db2 = pd.read_csv('C:/Users/User/DB2 Folder' + table, index_col=None, encoding='latin')
    print('C:/Users/User/DB1 Folder' + table)
    print('C:/Users/User/DB2 Folder' + table)
    ## standardise names
    db1.columns = db1.columns.str.lower()
    db2.columns = db2.columns.str.lower()

    ## fix potential difference in NULL values based on database standard
    #db1 = db1.replace('(null)', np.nan)
    #db2 = db2.replace('(null)', np.nan)

    ## Compare Data Frames
    delta = db1.compare(db2).rename(columns={'self': 'Database 1', 'other': 'Database 2'}, level=-1)

    ## append differences
    total_delta = total_delta.append(delta)
    print(table + ' db2 ' + str(len(db2.columns)) + ' db1 ' + str(len(db1.columns)))

    ## Write Excel, depending on how many rows are in the files locations need to be adjusted
    worksheet = workbook.add_worksheet(str(table[0:30]))
    writer.sheets[str(table[0:30])] = worksheet
    worksheet.write_string(0,0,'DB1')
    db1.to_excel(writer, sheet_name=str(table[0:30]), startrow=1, startcol=0)
    worksheet.write_string(db2.shape[0] + 4, 0 ,'DB2')
    db2.to_excel(writer, sheet_name=str(table[0:30]), startrow=db1.shape[0] + 5, startcol=0)
    worksheet.write_string(db2.shape[0] + db1.shape[0] + 4, 0 ,'Delta')
    delta.to_excel(writer, sheet_name=str(table[0:30]), startrow=db1.shape[0] + 7 + db1.shape[0], startcol=0)
    worksheet
    
workbook.close()
print('done')
