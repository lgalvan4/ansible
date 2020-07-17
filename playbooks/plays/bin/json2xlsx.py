import tablib

data = tablib.Dataset()
import_filename = '/tmp/report.json'
data.json = open(import_filename, 'r').read()

data_export = data.export('xlsx')

with open('/tmp/report.xlsx', 'wb') as f:  # open the xlsx file
    f.write(data_export)  # write the dataset to the xlsx file
f.close()