import tablib
import sys

inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])

data = tablib.Dataset()
imported_data = data.load(open(inputFile, 'r').read())

data_export = imported_data.export('xlsx')

with open(outputFile, 'wb') as f:
    f.write(data_export)
f.close()