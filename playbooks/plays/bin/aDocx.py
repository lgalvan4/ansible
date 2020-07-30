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
g_fufield='filtered_updates'
g_ctgfield='categories'
g_notWinfield="Windows"
g_Title_for_G="Updates"
g_Aspect_for_G="equal"
g_Font_for_G={'fontsize': "x-large",'fontweight': 7,}
nitemfield=0
g_ctu=0
g_ltu=[]
g_stu={}
inputFile = str(sys.argv[1])
outputFile = str(sys.argv[2])
host = str(sys.argv[3])
jsonFile = str(sys.argv[4])
with open(jsonFile) as f:
	g_dataG = json.load(f)
for elem in g_dataG[g_fufield]:
	for g_st in g_dataG[g_fufield][str(elem)][g_ctgfield]: 
		if g_st in g_ltu:
			g_stu[str(g_st)]=1+g_stu[str(g_st)]
			g_ctu=g_ctu+1
		if ((g_notWinfield not in g_st) and (g_st not in g_ltu)):
			g_ltu.append(str(g_st))
			g_stu[str(g_st)]=1
			g_ctu=g_ctu+1
fig, ax = plt.subplots(figsize=(9, 5), subplot_kw=dict(aspect=g_Aspect_for_G))
g_albls=[]
g_asizes=[]
for g_k in g_stu:
    g_albls.append(str(g_k))
    g_asizes.append(g_stu[str(g_k)])
g_labels = g_albls
g_fracs = g_asizes
fig = plt.figure(figsize=(8, 6))
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
g_explode = (0, 0,0,0)
g_pies = ax.pie(g_fracs, labels=g_labels, explode=g_explode, autopct='%.2f')
for w in g_pies[0]:
    w.set_gid(w.get_label())
    w.set_edgecolor("none")
for w in g_pies[0]:
    s = Shadow(w, -0.01, -0.01)
    s.set_gid(w.get_gid() + "_shadow")
    s.set_zorder(w.get_zorder() - 0.1)
    ax.add_patch(s)
ax.set_title(g_Title_for_G,fontdict=g_Font_for_G)
from io import BytesIO
f = BytesIO()
fig.savefig('report_categories_'+host+'.png')
