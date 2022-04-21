import networkx as nx
import itertools
import re
import os
from natsort import natsorted

import sys
path_ = sys.argv[1]
MaxpatternsNo = sys.argv[2]
MinpatternsLen = sys.argv[3]
MinpatternsFreq = sys.argv[4]

#overall folder
list_of_lists = []
for r in os.listdir('.'+path_):
    if r.endswith('.txt'):
        with open(os.path.join('.'+path_, r)) as f:
                clean = [re.sub(r' ', '', i) for i in f]
                list_of_lists.append(clean)

graph_sets = []
for r in os.listdir('./subgraphs-source'):
    if r.endswith('.txt'):
        with open(os.path.join('./subgraphs-source', r)) as f:
                clean = [re.sub(r' ', '', i) for i in f]
                graph_sets.append(clean)
                
subgraphs_sets = []
for r in os.listdir('./subgraphs-full'):
    if r.endswith('.txt'):
        with open(os.path.join('./subgraphs-full', r)) as f:
                clean = [re.sub(r' ', '', i) for i in f]
                subgraphs_sets.append(clean)

def nocard(x):
    ###filter_cardinalities###
    final0 =  [[re.sub(r'\"\*(.*?)\*', '"', item) for item in x] for x in x]
    final1 =  [[re.sub(r'\"[0-9](.*?)[0-9]', '"', item) for item in x] for x in final0]
    final2 =  [[re.sub(r'\"\*(.*?)[0-9]', '"', item) for item in x] for x in final1]
    final3 =  [[re.sub(r'\"[0-9](.*?)\*', '"', item) for item in x] for x in final2]
    final4 =  [[re.sub(r'\"\.(.*?)[0-9]', '"', item) for item in x] for x in final3]
    final5 =  [[re.sub(r'\"\.(.*?)\*', '"', item) for item in x] for x in final4]
    final6 =  [[re.sub(r'\"\*', '"', item) for item in x] for x in final5]
    final7 = [[re.sub(r'\"[0-9]', '"', item) for item in x] for x in final6]
    final8 = [[re.sub(r'nullnullnull', 'none', item) for item in x] for x in final7]
    final9 = [[re.sub(r'nullnull', '', item) for item in x] for x in final8]
    final10_ = [[re.sub(r'NoneNoneNone', '', item) for item in x] for x in final9]
    final10__ = [[re.sub(r'NoneNone', '', item) for item in x] for x in final10_]
    final10___ = [[re.sub(r'\"None', '"', item) for item in x] for x in final10__]
    final10____ = [[re.sub(r'[0-9]m', 'm', item) for item in x] for x in final10___] #
    final10 = [[re.sub(r'\n', '', item) for item in x] for x in final10____]
    ###filter_cardinalities###
    itemSetList = final10 #if we want cardinalities, just keep "final"
    r = re.compile('->')
    t = [[item for item in sublist if r.findall(item)] for sublist in itemSetList]
    return t

iSet = nocard(list_of_lists)
gSet = nocard(graph_sets)
sgSet = nocard(subgraphs_sets)
#print(nocard(list_of_lists))

#####seee here!!!
from prefixspan import PrefixSpan
ps = PrefixSpan(iSet)

patterns_set = ps.topk(MaxpatternsNo,closed=True) #generator
patterns_set_filtered = [i for i in patterns_set if len(i[1]) >= MinpatternsLen]
patterns_filter = [item for item in patterns_set_filtered if item[0] >= MinpatternsFreq] 
patterns_filter0 = [item[1] for item in patterns_filter]
occurrences = [item[0] for item in patterns_filter]

#THE ACCURACY is the number in "pattern filters" divided for the total amount of graphs, generated from subgraph generation
patternLists = natsorted(sum(patterns_filter0, []))
finalPattern = [item for i, item in enumerate(patternLists) if i == 0 or i == len(patternLists) or patternLists[i - 1] != item]
# print(patterns_filter0)
# print(gSet)

# final = []
# flag_ = 0
# for y in patterns_filter0:
#     output = []
#     final.append(output)
#     for z in gSet:
#         if(all(x in z for x in y)):
#             flag_ = 1
#             output.append(flag_)
# sums = [sum(sublist) for sublist in final]
# # for y in patterns_filter0:
# #     print(y)
# print(sums)

sums = []
for y in patterns_filter0:
    out = [sum(1 for i in range(len(x)) if x[i:i+len(y)]==y) for x in gSet]
    out0 = [x for x in out if x != 0]
    out1 = len(out0)
    sums.append(out1)

# final0 = []
# flag_0 = 0
# for y in patterns_filter0:
#     output0 = []
#     final0.append(output0)
#     for z in sgSet:
#         if(all(x in z for x in y)):
#             flag_0 = 1
#             output0.append(flag_0)
# sums0 = [sum(sublist) for sublist in final0]


mTuple = []
for i,j in list(zip(occurrences,sums)):
    if i < j:
        mTuple.append((j,j))
    else:
        mTuple.append((i,j))
        
def metrics(x):
    if '/subgraphs-full' in x:
        return mTuple
    else:
        return occurrences

metr_ = metrics(path_)      


# #make this FOR EACH DERIVED PATTERN, ONE BY ONE! FROM HERE
graphGenerationEdges =  [[re.sub(r'->', ' -> ', item) for item in x] for x in patterns_filter0]
graphGenerationAtt =  [[re.sub(r'\]', ']', item) for item in x] for x in graphGenerationEdges]
graphGenerationAttNull =  [[re.sub(r'ln', 'l-n', item) for item in x] for x in graphGenerationAtt]
graphGenerationAttNull0 = ['\n'.join(i) for i in graphGenerationAttNull]

#insert direction
firstOutput = ["digraph" + " " + "\"graph\"" + " " + "{\n"+"graph" + " " + "[fontsize=12]\n"+"node" + " " + "[fontsize=12]\n"+"edge" + " " + "[fontsize=12]\n"+"rankdir=BT;\n"+str(i)+"\n"+"}" for i in graphGenerationAttNull0]

import pygraphviz as pgv
import networkx as nx
from typing import List

directedGraph = []
for i in firstOutput:
    gv = pgv.AGraph(i,directed=True,data=True)
    D = nx.MultiDiGraph(gv,data=True)
    directedGraph.append(D)

directedGraphFrequency = list(zip(metr_,directedGraph))


###(WITH_INDEX)
unconnectedGraphs = []
for n,i in zip(metr_,directedGraph):
    for c in nx.weakly_connected_components(i):
        cg = n,i.subgraph(c).copy()
        unconnectedGraphs.append(cg)

# #####single-nodes#####
noEdge_f = []
for (n,g) in unconnectedGraphs: #here last filter
    if (n,g.number_of_edges() != 0):
        noEdge_f.append((n,g))
# #####single-nodes#####

noEdge = [g for n,g in noEdge_f]
frequencies = [n for n,g in noEdge_f]



# #####filter-unconnected#####
lostNodes = [[node for node in g.nodes() if g.in_degree(node)==0 and g.out_degree(node)==0] for (n,g) in noEdge_f]
removelostNodes = []
for (n,g),i in zip(noEdge_f,lostNodes):
    n,g.remove_nodes_from(i)
    removelostNodes.append((n,g))
# #####filter-unconnected#####

# # ######re-indexing labels for deliting duplicate graphs######
iLabels = []
for i in noEdge:
    iLabelsItem = i.nodes(data=True)
    iLabels.append(iLabelsItem)
dictIlabels = [dict(i) for i in iLabels]
names = [list(item.keys()) for item in dictIlabels]

namesNoNumber = [[re.sub(r'_(.*?)_', '', i) for i in sublist] for sublist in names]
res = [[list(i) for j, i in itertools.groupby(natsorted(sublist))] for sublist in namesNoNumber]
indexRes = [[[index[0] for index in enumerate(i)] for i in sublist] for sublist in res]
nameDictionary = [{a:c for a,c in zip(x,y)} for (x,y) in zip(names,namesNoNumber)]

sortedd = []
for x in nameDictionary:
    d = {k: v for k, v in natsorted(x.items(), key=lambda item: item[1])}
    sortedd.append(d)

listItems = [list(i.items()) for i in sortedd]
flatIndexRes = [[item for subsublist in sublist for item in subsublist] for sublist in indexRes]
finalZip = [[(a,b) for a,b in zip(x,y)] for x,y in zip(listItems,flatIndexRes)]
finalZip0 = [[(a,b+"_"+str(c)+"_") for (a,b), c in x] for x in finalZip]
newRenumberedDict = [{a:b for a,b in item} for item in finalZip0] #OOOOOK!!!

RelabeledGraphs = []
for x,y in zip(noEdge,newRenumberedDict):
    KK = nx.relabel_nodes(x, y)
    RelabeledGraphs.append(KK)
# ######re-indexing labels!######

intermediateOutput = []
for n,line in zip(frequencies, RelabeledGraphs):
    if line.number_of_edges() != 0:
        intermediateOutput.append((n,line))



import json
finalFrequencies = [f for f,i in intermediateOutput]
finalGraphs = [[x for x in i.edges(data=True)] for f,i in intermediateOutput]
finalGraphs0 = [json.dumps(i) for i in finalGraphs]


finalCombo = tuple(zip(finalGraphs0,finalFrequencies))


from collections import OrderedDict
d = OrderedDict()

for k, v in finalCombo:
    d.setdefault(k, []).append(v)
# for i in d.items():
#     print(i)

finalTupleList = [(i,max(f)) for i,f in d.items()]

finalDict = [[json.loads(i),f] for i,f in finalTupleList]

fGraphs = []
for i,f in finalDict:
    F = nx.DiGraph()
    F.add_edges_from(i)
    fGraphs.append((F,f))

stringpath = re.sub(r'/subgraphs-single/', '', path_) 
stringpath0 = re.sub(r'/subgraphs-', '', stringpath) 
  
outpath = "./output/"+stringpath0+"/"
exist = os.path.isdir(outpath)
if not exist:
    new_dir = os.mkdir(outpath)
else:
    print("")

def opath(x):    
    if './output/full/' in x:
        return "full"
    if './output/meta/' in x:
        return "meta"
    else:
        pattern2 = "\/output/(.*?)\.json"
        return re.search(pattern2, x).group(1)

namepath = opath(outpath)

for i, (graph,f) in enumerate(fGraphs):
    nx.drawing.nx_pydot.write_dot(graph,"{}{}-{}-{}.txt".format(outpath,namepath,f,i)) #change here the name

import glob
for file in glob.glob(outpath+'*txt'):
    with open(file.replace('.txt', '-out.txt'), 'w') as outfile:
        with open(file) as infile:
            text = infile.readlines()
            text.insert(1, "rankdir=BT;\n")
            outfile.write(''.join(text))

my_dir = outpath
for fname in os.listdir(outpath):
    if not fname.endswith("-out.txt"):
        os.remove(os.path.join(my_dir, fname))
        
# # # #visualization
from graphviz import Source
for r in os.listdir(outpath):
    if r.endswith('.txt'):
        f = os.path.join(outpath, r)
        g = nx.drawing.nx_agraph.read_dot(f)
        s = Source.from_file(f)
        s.render() #convert - pdf

stringCheck = '/subgraphs-single/'
import glob
if stringCheck in path_:
    for i, (graph,f) in enumerate(fGraphs):
        nx.drawing.nx_pydot.write_dot(graph,"./subgraphs-meta/{}-{}-{}.txt".format(namepath,f,i)) #change here the name

