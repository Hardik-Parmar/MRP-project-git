import pandas as pd
data_xls = pd.read_excel('/home/logicrays/Documents/Projects/Projects/records/Final_1/RBT_mar.xlsx', 'Sheet1', index_col=None)
data_xls.to_csv('/home/logicrays/Documents/Projects/Projects/records/Final_1/RBT_mar2.csv', encoding='utf-8')