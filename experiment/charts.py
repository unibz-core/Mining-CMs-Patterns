from cProfile import label
import seaborn as sns
import pandas
import matplotlib.pyplot as plt
import numpy as np

# libraries
import numpy as np
from numpy import linspace
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.ticker import MaxNLocator


main = pandas.read_csv(r'trial1.csv')
phase= main.loc[main['pattern'] == 'phase'].sort_values('sort')
roleMixin= main.loc[main['pattern'] == 'roleMixin'].sort_values('sort')
characterization= main.loc[main['pattern'] == 'characterization'].sort_values('sort')
subkind= main.loc[main['pattern'] == 'subkind'].sort_values('sort')
relator= main.loc[main['pattern'] == 'relator'].sort_values('sort')
category= main.loc[main['pattern'] == 'category'].sort_values('sort')


matplotlib.rc_file_defaults()
axes = sns.set_style(style=None, rc=None )
fig, axes = plt.subplots(4, 3, figsize=(12, 12))

#axes.set_xlim(left=0, right=5)
axes[0,0].set_ylim(bottom=0, top=28)
axes[0,1].set_ylim(bottom=0, top=55)
axes[0,2].set_ylim(bottom=0, top=25)
#
axes[1,0].set_ylim(bottom=0, top=143) 
axes[1,1].set_ylim(bottom=0, top=43)
axes[1,2].set_ylim(bottom=0, top=53)
#
axes[0,0].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[0,1].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[0,2].yaxis.set_major_locator(MaxNLocator(integer=True))
#
axes[1,0].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[1,1].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[1,2].yaxis.set_major_locator(MaxNLocator(integer=True))

#########

axes[2,0].set_ylim(bottom=0, top=18)
axes[2,1].set_ylim(bottom=0, top=18)
axes[2,2].set_ylim(bottom=0, top=8)
#
axes[3,0].set_ylim(bottom=0, top=60)
axes[3,1].set_ylim(bottom=0, top=20)
axes[3,2].set_ylim(bottom=0, top=38)
#
axes[2,0].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[2,1].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[2,2].yaxis.set_major_locator(MaxNLocator(integer=True))
#
axes[3,0].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[3,1].yaxis.set_major_locator(MaxNLocator(integer=True))
axes[3,2].yaxis.set_major_locator(MaxNLocator(integer=True))

font = {#'family': 'serif',
        'color':  'blue',
        'weight': 'bold',
        'size': 9
        }

# #phase
a = sns.barplot(ax=axes[0,0], data=phase, x='trials', 
                y='absolute_frequency',ci=None,palette = 'magma',alpha=0.4,edgecolor = "black")

a.axhline(22, color="red", label="tot. = 22",linestyle='--')
a.legend(loc='upper right')

for container in a.containers:
    a.bar_label(container)
    a.set_title('phase pattern')

ax1 = axes[0,0].twinx()
ax1.set_ylim(bottom=0, top=2.8)
ax1.yaxis.set_visible(False)
a1 = sns.lineplot(ax=ax1, data=phase,x='trials',
                  y='jaccard',ci=None,color="blue",marker='o')
plt.legend(title='', loc='upper left', labels=['JIndex'])
#sns.move_legend(a1,"lower center",bbox_to_anchor=(.5, 1))

a1.set(xlabel=None)
a.set(xlabel=None)

for x,y in phase[['trials','jaccard']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=40)

# #roleMixin
b = sns.barplot(ax=axes[0,1], data=roleMixin, x='trials',
                y='absolute_frequency',ci=None,palette = 'magma',alpha=0.4,edgecolor = "black")

b.axhline(44, color="red", label="tot. = 44",linestyle='--')
b.legend(loc='upper left')

for container in b.containers:
    b.bar_label(container)
    b.set_title('roleMixin pattern')

ax2 = axes[0,1].twinx()
ax2.set_ylim(bottom=0, top=2.8)
ax2.yaxis.set_visible(False)
b1 = sns.lineplot(ax=ax2, data=roleMixin,x='trials',
                 y='jaccard',ci=None,color="blue",marker='o')
b1.set(xlabel=None)
b.set(xlabel=None)
b1.set(ylabel=None)
b.set(ylabel=None)

for x,y in roleMixin[['trials','jaccard']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)
    #plt.text(x,y+0.02,y,fontdict=font)

# #characterization
c = sns.barplot(ax=axes[0,2], data=characterization, x='trials',
                y='absolute_frequency',ci=None,palette = 'magma',alpha=0.4,edgecolor = "black")

c.axhline(20, color="red", label="tot. = 20",linestyle='--')
c.legend(loc='upper left')

for container in c.containers:
    c.bar_label(container)
    c.set_title('characterization pattern')

ax3 = axes[0,2].twinx()
ax3.set_ylim(bottom=0, top=2.8)
ax3.yaxis.set_visible(False)
#ax3.xaxis.set_visible(False)
c1 = sns.lineplot(ax=ax3, data=characterization,x='trials',
                 y='jaccard',ci=None,color="blue",marker='o')
#plt.legend(title='', loc='upper left', labels=['Jaccard Index'])
c1.set(xlabel=None)
c.set(xlabel=None)
c1.set(ylabel=None)
c.set(ylabel=None)

for x,y in characterization[['trials','jaccard']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)
    #plt.text(x,y+0.02,y,fontdict=font)
    
#subkind
d = sns.barplot(ax=axes[1,0], data=subkind, x='trials',
                y='absolute_frequency',ci=None,palette = 'magma',alpha=0.4,edgecolor = "black")
for container in d.containers:
    d.bar_label(container)
    d.set_title('subkind pattern')

d.axhline(116, color="red", label="tot. = 116",linestyle='--')
d.legend(loc='upper left')

ax4 = axes[1,0].twinx()
ax4.set_ylim(bottom=0, top=2.8)
ax4.yaxis.set_visible(False)
d1 = sns.lineplot(ax=ax4, data=subkind,x='trials',
                 y='jaccard',ci=None,color="blue",marker='o')
#plt.legend(title='', loc='upper left', labels=['Jaccard Index'])

d1.set(xlabel=None)
d.set(xlabel=None)

for x,y in subkind[['trials','jaccard']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)#rotation=45)
    #plt.text(x,y+0.02,y,fontdict=font)
    
# #relator
e = sns.barplot(ax=axes[1,1], data=relator, x='trials',
                y='absolute_frequency',ci=None,palette = 'magma',alpha=0.4,edgecolor = "black")
for container in e.containers:
    e.bar_label(container)
    e.set_title('relator pattern')

e.axhline(34, color="red", label="tot. = 34",linestyle='--')
e.legend(loc='upper left')

ax5 = axes[1,1].twinx()
ax5.set_ylim(bottom=0, top=2.8)
ax5.yaxis.set_visible(False)
e1 = sns.lineplot(ax=ax5, data=relator,x='trials',
                 y='jaccard',ci=None,color="blue",marker='o')

e1.set(xlabel=None)
e.set(xlabel=None)
e1.set(ylabel=None)
e.set(ylabel=None)

for x,y in relator[['trials','jaccard']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=40)#rotation=45)
    #plt.text(x,y+0.02,y,fontdict=font)

#category
f = sns.barplot(ax=axes[1,2], data=category, x='trials',
                y='absolute_frequency',ci=None,palette = 'magma',alpha=0.4,edgecolor = "black")
for container in f.containers:
    f.bar_label(container)
    f.set_title('category pattern')

f.axhline(43, color="red", label="tot. = 43",linestyle='--')
f.legend(loc='upper left')

ax6 = axes[1,2].twinx()
ax6.set_ylim(bottom=0, top=2.8)
ax6.yaxis.set_visible(False)
f1 = sns.lineplot(ax=ax6, data=category,x='trials',
                 y='jaccard',ci=None,color="blue",marker='o')

f1.set(xlabel=None)
f.set(xlabel=None)
f1.set(ylabel=None)
f.set(ylabel=None)

for x,y in category[['trials','jaccard']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)#rotation=45)
    #plt.text(x,y+0.02,y,fontdict=font)

font = {#'family': 'serif',
        'color':  'purple',
        'weight': 'bold',
        'size': 9
        }

# #phaseModels
am = sns.barplot(ax=axes[2,0], data=phase, x='trials', 
                y='models_frequency',ci=None,palette = 'viridis',alpha=0.4,edgecolor = "black")

am.axhline(14, color="red", label="tot. = 14",linestyle='--')
am.legend(loc='upper right')

for container in am.containers:
    am.bar_label(container)
    am.set_title('phase pattern')

ax1m = axes[2,0].twinx()
ax1m.set_ylim(bottom=0, top=2.8)
ax1m.yaxis.set_visible(False)
a1m = sns.lineplot(ax=ax1m, data=phase,x='trials',
                  y='jaccardM',ci=None,color="purple",marker='o')
plt.legend(title='', loc='upper left', labels=['JIndexM'])
#sns.move_legend(a1,"lower center",bbox_to_anchor=(.5, 1))

a1m.set(xlabel=None)
am.set(xlabel=None)

for x,y in phase[['trials','jaccardM']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=40)
    
    
# #roleMixinModels
# check the model frequency 13 instead of 14!
bm = sns.barplot(ax=axes[2,1], data=roleMixin, x='trials',
                y='models_frequency',ci=None,palette = 'viridis',alpha=0.4,edgecolor = "black")

bm.axhline(13, color="red", label="tot. = 13",linestyle='--')
bm.legend(loc='upper left')

for container in bm.containers:
    bm.bar_label(container)
    bm.set_title('roleMixin pattern')

ax2m = axes[2,1].twinx()
ax2m.set_ylim(bottom=0, top=2.8)
ax2m.yaxis.set_visible(False)
b1m = sns.lineplot(ax=ax2m, data=roleMixin,x='trials',
                 y='jaccardM',ci=None,color="purple",marker='o')
b1m.set(xlabel=None)
bm.set(xlabel=None)
b1m.set(ylabel=None)
bm.set(ylabel=None)

for x,y in roleMixin[['trials','jaccardM']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)
    #plt.text(x,y+0.02,y,fontdict=font)

# #characterizationModels
cm = sns.barplot(ax=axes[2,2], data=characterization, x='trials',
                y='models_frequency',ci=None,palette = 'viridis',alpha=0.4,edgecolor = "black")

cm.axhline(6, color="red", label="tot. = 6",linestyle='--')
cm.legend(loc='upper left')

for container in cm.containers:
    cm.bar_label(container)
    cm.set_title('characterization pattern')

ax3m = axes[2,2].twinx()
ax3m.set_ylim(bottom=0, top=2.8)
ax3m.yaxis.set_visible(False)
#ax3.xaxis.set_visible(False)
c1m = sns.lineplot(ax=ax3m, data=characterization,x='trials',
                 y='jaccardM',ci=None,color="purple",marker='o')
#plt.legend(title='', loc='upper left', labels=['Jaccard Index'])
c1m.set(xlabel=None)
cm.set(xlabel=None)
c1m.set(ylabel=None)
cm.set(ylabel=None)

for x,y in characterization[['trials','jaccardM']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)
    #plt.text(x,y+0.02,y,fontdict=font)
    
#subkindModels
dm = sns.barplot(ax=axes[3,0], data=subkind, x='trials',
                y='models_frequency',ci=None,palette = 'viridis',alpha=0.4,edgecolor = "black")
for container in dm.containers:
    dm.bar_label(container)
    dm.set_title('subkind pattern')

dm.axhline(46, color="red", label="tot. = 46",linestyle='--')
dm.legend(loc='upper left')

ax4m = axes[3,0].twinx()
ax4m.set_ylim(bottom=0, top=2.8)
ax4m.yaxis.set_visible(False)
d1m = sns.lineplot(ax=ax4m, data=subkind,x='trials',
                 y='jaccardM',ci=None,color="purple",marker='o')
#plt.legend(title='', loc='upper left', labels=['Jaccard Index'])

for x,y in subkind[['trials','jaccardM']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)#rotation=45)
    #plt.text(x,y+0.02,y,fontdict=font)

# #relatorModels
em = sns.barplot(ax=axes[3,1], data=relator, x='trials',
                y='models_frequency',ci=None,palette = 'viridis',alpha=0.4,edgecolor = "black")
for container in em.containers:
    em.bar_label(container)
    em.set_title('relator pattern')

em.axhline(16, color="red", label="tot. = 16",linestyle='--')
em.legend(loc='upper left')

ax5m = axes[3,1].twinx()
ax5m.set_ylim(bottom=0, top=2.8)
ax5m.yaxis.set_visible(False)
e1m = sns.lineplot(ax=ax5m, data=relator,x='trials',
                 y='jaccardM',ci=None,color="purple",marker='o')

e1m.set(ylabel=None)
em.set(ylabel=None)

for x,y in relator[['trials','jaccardM']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=40)#rotation=45)
    #plt.text(x,y+0.02,y,fontdict=font)
    
#categoryModel
fm = sns.barplot(ax=axes[3,2], data=category, x='trials',
                y='models_frequency',ci=None,palette = 'viridis',alpha=0.4,edgecolor = "black")
for container in fm.containers:
    fm.bar_label(container)
    fm.set_title('category pattern')

fm.axhline(30, color="red", label="tot. = 30",linestyle='--')
fm.legend(loc='upper left')

ax6 = axes[3,2].twinx()
ax6.set_ylim(bottom=0, top=2.8)
ax6.yaxis.set_visible(False)
f1m = sns.lineplot(ax=ax6, data=category,x='trials',
                 y='jaccardM',ci=None,color="purple",marker='o')

f1m.set(ylabel=None)
fm.set(ylabel=None)

for x,y in category[['trials','jaccardM']].values:
    plt.text(x,y+0.07,y,fontdict=font,rotation=35)#rotation=45)
    #plt.text(x,y+0.02,y,fontdict=font)

plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.2, 
                    hspace=0.3)

#plt.show()
plt.savefig("final.pdf", bbox_inches='tight')


