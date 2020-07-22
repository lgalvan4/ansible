import sys
import datetime
from os import path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt

inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])
host = str(sys.argv[3])
os = str(sys.argv[4])
sp = str(sys.argv[5])
ip = str(sys.argv[6])

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
    ('Service Pack', sp),
    ('IP Address', ip),
    ('Last Status Reported', datetime.datetime.now())
)

table = document.add_table(rows=1, cols=2)
hdr_cells = table.rows[0].cells
hdr_cells[0].text = 'Id'
hdr_cells[1].text = 'Valor'
for id, val in records:
    row_cells = table.add_row().cells
    row_cells[0].text = id
    row_cells[1].text = val

document.save(outputFile)