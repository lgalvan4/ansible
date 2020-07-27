import sys
import datetime
from os import path
import json

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE

#Leyendo parametros
inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])
host = str(sys.argv[3])
#os = str(sys.argv[4])
#sp = str(sys.argv[5])
#ip = str(sys.argv[6])
jsonFile = str(sys.argv[4])

#--Loading json file, cleaning useless columns to have an easier json file to work with

with open(jsonFile) as data_file:
    da = json.load(data_file)
    data = json.dumps(da['updates'])
    duckingUpdates = json.loads(data)

#--Taking KB Information out of the title to avoid displaying duplicated info

for ftitle in duckingUpdates.values():
    borrarKB = ftitle['title']
    kbBorrado = borrarKB.rsplit(' ', 1)[0]
    ftitle['title'] = kbBorrado

#--Getting Os Name
iterator = iter(duckingUpdates.values())
first_value = next(iterator)
os = first_value['categories'][1]

#os = 'Windows Server 2008 R2'

#Verificando archivo a editar
if ( not path.exists(outputFile) ):
    #No existe outputfile, abriendo plantilla
    document = Document(inputFile)
else:
    #Abriendo outputfile
    document = Document(outputFile)

#Si el archivo de salida existe, no se agrega portada
if ( not path.exists(outputFile) ):

    #Creando Portada
    parrafo = document.add_paragraph()
    run = parrafo.add_run('Reporte de Actualizaciones Windows')
    font = run.font
    font.size = Pt(24)
    font.bold = True
    formato_parrafo = parrafo.paragraph_format
    formato_parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    document.add_paragraph()

    parrafo = document.add_paragraph()
    run = parrafo.add_run('Inventario: Prueba')
    font = run.font
    font.size = Pt(24)
    font.bold = True
    formato_parrafo = parrafo.paragraph_format
    formato_parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

    document.add_paragraph()

    parrafo = document.add_paragraph()
    run = parrafo.add_run('Julio 2020')
    font = run.font
    font.size = Pt(24)
    font.bold = True
    formato_parrafo = parrafo.paragraph_format
    formato_parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

#introduciendo informacion

document.add_page_break() #Salto de Pagina

document.add_paragraph() #Enter 

parrafo = document.add_paragraph()
run = parrafo.add_run('Servidor: ' +host)
font = run.font
font.size = Pt(14)
font.bold = True
formato_parrafo = parrafo.paragraph_format
formato_parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

document.add_paragraph() #Enter

parrafo = document.add_paragraph()
run = parrafo.add_run('Detalles del servidor:')

document.add_paragraph() #Enter

records = (
    ('Operating System', os),
    ('Service Pack', 'None'),
    ('Host Name', host),
    ('Last Status Reported', str(datetime.datetime.now()))
)

table = document.add_table(rows=1, cols=2)
table.style = document.styles['Light List Accent 6']
#table.style = "Table Grid"
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Id'
hdr_cells[1].text = 'Valor'
for id, val in records:
    row_cells = table.add_row().cells
    row_cells[0].text = id
    row_cells[1].text = val

document.add_paragraph() #Enter
document.add_paragraph() #Enter

#Adding Graph iside a table
table_graph = document.add_table(rows=1, cols=2)

#Celda de imagen
pic_cells = table_graph.rows[0].cells
pic_cell = pic_cells[0]
run = pic_cell.add_paragraph().add_run()
run.add_picture('2020-07-24.png', width=Inches(3))

#Celda de texto 
tx_cells = table_graph.rows[0].cells
tb_cell_run = tx_cells[1].add_paragraph().add_run()
tb_cell_run.add_text('170 Updates encontradas \n 50 Criticas \n 3 Fixes')

#tb_cell_run.font.size =  Pt(8)

document.add_paragraph() #Enter
document.add_paragraph() #Enter

#--Creating table - Autofit didn't work - setting up columns width manually
reportTable = document.add_table(rows=1, cols=4)
reportTable.autofit = True
reportTable.style = 'Colorful Shading Accent 6'
hdr_Cells = reportTable.rows[0].cells
hdr_Cells[0].width = Inches(0.48) 
hdr_Cells[0].text = 'KB'
hdr_Cells[1].width = Inches(4.45)
hdr_Cells[1].text = 'Title'
hdr_Cells[2].width = Inches(0.77)
hdr_Cells[2].text = 'Category'
hdr_Cells[3].width = Inches(0.45)
hdr_Cells[3].text = 'Installed'

#--Filling up table

for fvalue in duckingUpdates.values():
    row_Cells = reportTable.add_row().cells
    row_Cells[0].width = Inches(0.48)
    row_Cells[0].text = fvalue['kb']
    row_Cells[1].width = Inches(4.45)
    row_Cells[1].text = fvalue['title']
    row_Cells[2].width = Inches(0.77)
    row_Cells[2].text = fvalue['categories'][0]
    row_Cells[3].width = Inches(0.45)
    row_Cells[3].text = str(fvalue['installed'])

#-- Setting font size for the whole table.

for row in reportTable.rows:
    for cell in row.cells:
        paragraphs = cell.paragraphs
        paragraph = paragraphs[0]
        run_obj = paragraph.runs
        run = run_obj[0]
        font = run.font
        font.size = Pt(5.5)

#adding Detail
# records = (
#     ('2018-10 Update for Windows Server 2008 R2 for x64-based Systems (KB3177467)', 'Security Updates', 'Install', 'Not Installed'),
#     ('2018-12 Security and Quality Rollup for .NET Framework 3.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2 for Windows 7 and Server 2008 R2 for x64 (KB4471987)', 'Security Updates', 'Install',	'Not Installed'),
#     ('2019-01 Security and Quality Rollup for .NET Framework 3.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2 for Windows 7 and Server 2008 R2 for x64 (KB4481480)', 'Update Rollups', 'Install', 'Not Installed'),
#     ('2019-01 Security Only Update for .NET Framework 3.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2 for Windows 7 and Server 2008 R2 for x64 (KB4481481)', 'Feature Packs', 'Install', 'Not Installed'),
#     ('2019-02 Security and Quality Rollup for .NET Framework 3.5.1, 4.5.2, 4.6, 4.6.1, 4.6.2, 4.7, 4.7.1, 4.7.2 for Windows 7 and Server 2008 R2 for x64 (KB4487078)', 'Critical Updates', 'Install', 'Not Installed')
# )
# #Creando Tabla
# table = document.add_table(rows=1, cols=4)
# #Dando Formato
# table.style = document.styles['Medium Shading 1 Accent 6']
# table.allow_autofit = True
# #Ingresando titulos
# hdr_cells = table.rows[0].cells
# hdr_cells[0].text = 'Title'
# hdr_cells[1].text = 'Classification'
# hdr_cells[2].text = 'Aproval'
# hdr_cells[3].text = 'Status'
# #Poblando Tabla
# # for title, clas, aprov, status in records:
# #     row_cells = table.add_row().cells
# #     row_cells[0].text = title
# #     row_cells[1].text = clas
# #     row_cells[2].text = aprov
# #     row_cells[3].text = status

# for title, clas, aprov, status in records:
#     row_cells = table.add_row().cells

#     #row_cells[0].text = title
#     tb_cell_run0 = row_cells[0].add_paragraph().add_run()
#     tb_cell_run0.add_text(title)
#     tb_cell_run0.font.size =  Pt(8)

#     #row_cells[1].text = clas
#     tb_cell_run1 = row_cells[1].add_paragraph().add_run()
#     tb_cell_run1.add_text(clas)
#     tb_cell_run1.font.size =  Pt(8)

#     #row_cells[2].text = aprov
#     tb_cell_run2 = row_cells[2].add_paragraph().add_run()
#     tb_cell_run2.add_text(aprov)
#     tb_cell_run2.font.size =  Pt(8)

#     #row_cells[3].text = status
#     tb_cell_run3 = row_cells[3].add_paragraph().add_run()
#     tb_cell_run3.add_text(status)
#     tb_cell_run3.font.size =  Pt(8)


document.save(outputFile)