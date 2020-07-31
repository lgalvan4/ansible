import sys
import datetime
from os import path
import json

#python-docx
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Pt
from docx.shared import Inches
from docx.enum.style import WD_STYLE_TYPE

#Matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Shadow

#Color Generator
from faker import Faker
fake = Faker()

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

table = document.add_table(rows=0, cols=2)
table.style = document.styles['Medium Grid 1 Accent 1']
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
table_graph = document.add_table(rows=1, cols=1)

#Celda de imagen
# pic_cells = table_graph.rows[0].cells
# pic_cell = pic_cells[0]
# run = pic_cell.add_paragraph().add_run()
# picture_path='/tmp/report_'+host+'.png'
# run.add_picture(picture_path, width=Inches(3))

#Celda de texto
pic_cells2 = table_graph.rows[0].cells
pic_cells2_pag = pic_cells2[0].add_paragraph()
pic_cells2_pag.alignment=WD_ALIGN_PARAGRAPH.CENTER
pic_cells2_run=pic_cells2_pag.add_run()
#pic_cells2_run.add_picture(picture_path, width=Inches(3))

#tb_cell_run.font.size =  Pt(8)

document.add_paragraph() #Enter
document.add_paragraph() #Enter

#--Creating table - Autofit didn't work - setting up columns width manually
reportTable = document.add_table(rows=1, cols=4)
#reportTable.autofit = False
#reportTable.style = 'Colorful Shading Accent 6'
reportTable.style = 'Medium Grid 1 Accent 1'
hdr_Cells = reportTable.rows[0].cells
#hdr_Cells[0].width = Inches(0.48) 
hdr_Cells[0].text = 'KB'
#hdr_Cells[1].width = Inches(4.45)
hdr_Cells[1].text = 'Title'
#hdr_Cells[2].width = Inches(0.77)
hdr_Cells[2].text = 'Category'
#hdr_Cells[3].width = Inches(0.45)
hdr_Cells[3].text = 'Installed'

#--Filling up table
catgories_dict = {}

for fvalue in duckingUpdates.values():
    row_Cells = reportTable.add_row().cells
    #row_Cells[0].width = Inches(0.48)
    row_Cells[0].text = fvalue['kb']
    #row_Cells[1].width = Inches(4.45)
    row_Cells[1].text = fvalue['title']
    #row_Cells[2].width = Inches(0.77)
    row_Cells[2].text = fvalue['categories'][0] #count sobre esta linea
    #row_Cells[3].width = Inches(0.45)
    row_Cells[3].text = str(fvalue['installed'])

    if fvalue['categories'][0] in catgories_dict:
        catgories_dict[fvalue['categories'][0]] = catgories_dict.get(fvalue['categories'][0])+1
    else:
        catgories_dict[fvalue['categories'][0]] = 1

#print(catgories_dict)

# colores random
fcolor = fake.hex_color()

#Creando vectores
titulos = []
contadores = []
explod = []
fcolors = []
for t, c in catgories_dict.items():
    titulos.append(t+' '+str(c))
    contadores.append(c)
    explod.append(0.05)

    if t == 'Critical Updates':
        fcolors.append("#EC1E1E")
    elif t == 'Security Updates':
        fcolors.append("#F3951C")
    elif t == 'Update Rollups':
        fcolors.append("#2672BF")
    elif t == 'Updates':
        fcolors.append("#48B14B")
    elif t == 'Service Packs':
        fcolors.append("#F6F167")
    else:
        fcolors.append(fcolor)

#print(titulos)
#print(contadores)
#print(explode)

labels2=tuple(titulos)
fig1 = plt.figure(frameon=False )
ax1 = fig1.add_axes([0, 0.2, 0.6, 0.6])
patches, texts = ax1.pie(contadores, explode=tuple(explod), colors=tuple(fcolors), shadow=True, startangle=90)
#ax1.pie(contadores, explode=tuple(explod), labels=tuple(titulos), colors=tuple(fcolors) autopct='%1.1f%%', shadow=True, startangle=90)
ax1.legend(patches, labels2, 
           loc="center left",
           prop={'size': 15},
           bbox_to_anchor=(1, 0, 0.5, 1))  # Equal aspect ratio ensures that pie is drawn as a circle.

#plt.show()
fig1.savefig('/tmp/report_'+host+'2.png', bbox_inches='tight', pad_inches=0)

picture_path='/tmp/report_'+host+'2.png'
pic_cells2_run.add_picture(picture_path, width=Inches(4))
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