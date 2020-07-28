import sys
import datetime
from os import path
import json

#python-docx
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE

#Matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Shadow

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

#Graph
fig = plt.figure(figsize=(6, 6))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
labels = 'found_update_count', 'installed_update_count'

foundupdate_count=da['found_update_count']
installed_update_count=da['installed_update_count']

fracs = [foundupdate_count, installed_update_count]

explode = (0, 0.05)
pies = ax.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%')
for w in pies[0]:
    w.set_gid(w.get_label())
    w.set_edgecolor("none")
for w in pies[0]:
    s = Shadow(w, -0.01, -0.01)
    s.set_gid(w.get_gid() + "_shadow")
    s.set_zorder(w.get_zorder() - 0.1)
    ax.add_patch(s)
from io import BytesIO
f = BytesIO()
fig.savefig('/tmp/report_'+host+'.png')

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

    # parrafo = document.add_paragraph()
    # run = parrafo.add_run('Inventario: Prueba')
    # font = run.font
    # font.size = Pt(24)
    # font.bold = True
    # formato_parrafo = parrafo.paragraph_format
    # formato_parrafo.alignment = WD_ALIGN_PARAGRAPH.CENTER

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
#hdr_cells = table.rows[0].cells
#hdr_cells[0].text = 'Id'
#hdr_cells[1].text = 'Valor'
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
picture_path='/tmp/report_'+host+'.png'
run.add_picture(picture_path, width=Inches(3))

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
    row_Cells[2].text = fvalue['categories'][0] #count sobre esta linea
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

document.save(outputFile)