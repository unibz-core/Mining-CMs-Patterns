# %%

import networkx as nx
import itertools
import re
import os
from natsort import natsorted
from scraping.scraper import ontoUMLjsonA, ontoUMLjsonB

import sys
fileName = sys.argv[1]
isaW = sys.argv[2]
relW = sys.argv[3]
partitionValue = sys.argv[4]
edgeTypes = sys.argv[5]
normNodeType = sys.argv[6]
normEdgeType = sys.argv[7]
typeList = sys.argv[8]
relList = sys.argv[9]

if len(ontoUMLjsonA('./models/{}'.format(fileName))[0]) == 0:
    classes = ontoUMLjsonB('./models/{}'.format(fileName))[0]
    associations = ontoUMLjsonB('./models/{}'.format(fileName))[1]
    generalizations = ontoUMLjsonB('./models/{}'.format(fileName))[2]
else:
    classes = ontoUMLjsonA('./models/{}'.format(fileName))[0]
    associations = ontoUMLjsonA('./models/{}'.format(fileName))[1]
    generalizations = ontoUMLjsonA('./models/{}'.format(fileName))[2] 

classesNorm = [(a,b,'class') for a,b,c in classes]
classesFilter = [(a,b,c) for a,b,c in classes if c in typeList]

def normT(x): 
    if 'ste' in x:
        return classes
    if 'class' in x: 
        return classesNorm
    if 'fil' in x:
        return classesFilter

norm = normT(normNodeType)

print("Graph name:", fileName)

### Dictionaries for generating the graph
classesDict = {a:b for a,b,c in norm}
classesNodesDict = {a:c for a,b,c in norm} #b = domain, c = generalized

# store the names (the keys of the new dict) as a set (keeps elements unique)
names = set(classesNodesDict.values())
groupClasses = [[i for i in norm if x in i] for x in names]
indexListTypes = [[index[0] for index in enumerate(i)] for i in groupClasses]
classesNodesDictIndexType = [{a:c+"_"+str(j)+"_" for (a,b,c),j in zip(x,y)} for x,y in zip(groupClasses,indexListTypes)]


# %%

classesNodesDictIndexTypeOutput = {}
for d in classesNodesDictIndexType:
    classesNodesDictIndexTypeOutput.update(d)

indexList = [index[0] for index in enumerate(norm)]
classesNodesDictIndex = {a:c+"_"+str(j)+"_" for (a,b,c),j in zip(norm,indexList)}
generalizationNodesDict = {c:"ISA" for a,b,c in generalizations}
indexListGen = [index[0] for index in enumerate(generalizations)]
generalizationNodesDictIndex = {c:"ISA"+"_"+str(j)+"_" for (a,b,c),j in zip(generalizations,indexListGen)}

#look at the direction!
generalizationEdgesDictA = [[b, a, {"attribute":"ISA"}] for a,b,c in generalizations]
associationEdgesDict = [[a, b, {"attribute":d+" "+e+" "+f}] for a,b,c,d,e,f in associations] #the domain name needs to be extracted
justEdges = [[a, b, {"attribute":d+" "+e+" "+"relation"}] for a,b,c,d,e,f in associations] #the domain name needs to be extracted
relationsFilter = [[a, b, {"attribute":d+" "+e+" "+f}] for a,b,c,d,e,f in associations if f in relList]

def normRel(x): 
    if 'ste' in x:
        return associationEdgesDict
    if 'rel' in x: 
        return justEdges
    if 'fil' in x: 
        return relationsFilter

normRel(normEdgeType)

#### Generate graph
G = nx.MultiDiGraph(directed=True)

#### Graph nodes
try:
    Graph_Nodes = {**classesNodesDict}
except NameError:
    Graph_Nodes = {**classesNodesDict}

G.add_nodes_from(Graph_Nodes.keys())
for key,n in G.nodes.items():
   n["attribute"] = Graph_Nodes[key]

#### ADD_GRAPH_EDGES!!        
def edges(x): 
    if 'gen' in x:
        return G.add_edges_from(generalizationEdgesDictA)
    if 'rel' in x: 
        return G.add_edges_from(normRel(normEdgeType))
    if 'both' in x:
        return G.add_edges_from(normRel(normEdgeType)), G.add_edges_from(generalizationEdgesDictA)
edges(edgeTypes)

# #### FILTER nodes and EDGES    
L = nx.MultiDiGraph(G)
m = [L.remove_node(x) for x,y in G.nodes(data=True) if len(y) == 0]
# for x,y in L.nodes(data=True):
#     print(x,y)
      
# #ASSIGN_WEIGHTS
for s,t,a in L.edges(data=True):
    for i in L[s][t]:
        if i == 0:
            if a["attribute"] == "ISA":
                L[s][t][i]['weight'] = isaW
            else:
                L[s][t][i]['weight'] = relW
        else:
            L[s][t][i]['weight'] = relW

print("Graph: ", L)
print("Original graph nodes no.: ", len(L.nodes()))
print("Original graph edges no.: ", len(L.edges()))

# # %%

# # Unidirected Bisection partition
pos = nx.nx_pydot.graphviz_layout(L)
print("<---------------------------->")
node_labels = nx.get_node_attributes(L, 'attribute')
edges_labels_A = nx.get_edge_attributes(L,'attribute')

selected_nodes = []
for n,v in L.nodes(data=True):
    test = n
    selected_nodes.append(test)
G2 = L.to_undirected()

ls = []
def mergeSort(X):
    #print("Splitting ",X)
    #ls.append(X)
    if X.number_of_nodes() >= partitionValue: 
        partition = [list(i) for i in nx.algorithms.community.kernighan_lin_bisection(X, partition=None, max_iter=100, weight='weight', seed=100)]
        lefthalf = X.subgraph(partition[0])
        righthalf = X.subgraph(partition[1])
        mergeSort(lefthalf)
        mergeSort(righthalf)
    else:
        ls.append(X) 
X = G2
mergeSort(X)

print("Bisection subgraph partition:")

for i, sub in enumerate(ls):
    print("Bisection_Subgraph_{}:".format(i),sub)

sub_len_no = [len(i.nodes()) for i in ls]
print("partition total graph nodes no.: ", sum(sub_len_no))
sub_len_edg = [len(i.edges()) for i in ls]
print("partition total graph edges no.: ", sum(sub_len_edg)) 
print("<---------------------------->")

# # %%
# Drop graphs with no edges
H_list_NoEmpty = []
for x in ls:  
    if x.number_of_edges() != 0:
        H_list_NoEmpty.append(x)

# # %%
# Subgraph partition with all added edges
H_list = []
for x in H_list_NoEmpty: #here keep ls to keep with also no edges
    H = {}
    H[x] = nx.MultiDiGraph(directed=True)
    H[x].add_nodes_from(x.nodes(data=True))
    H[x].add_edges_from(L.edges(x,data=True))
    H_list.append(H[x])

# # %%
# #Labeled graph
labeled_graphs = []
for i in H_list: #"H_list" if full edges, "Graph_list" if bisection edges only
    try:
        F = nx.relabel_nodes(i, classesNodesDictIndexTypeOutput)
        labeled_graphs.append(F) 
    except NameError:
        F = nx.relabel_nodes(i, classesNodesDictIndexTypeOutput)
        labeled_graphs.append(F) 

# #DISCONNECT#
import pygraphviz as pgv
import networkx as nx
from typing import List

unconnectedGraphs = [] 
for n in labeled_graphs:
    for c in nx.weakly_connected_components(n):
        cg = n.subgraph(c).copy()
        unconnectedGraphs.append(cg)

H_list_NoEmpty0 = []
for x in unconnectedGraphs:  
    if x.number_of_edges() != 0:
        H_list_NoEmpty0.append(x)

# # %%
######re-indexing labels###### - key phase where we normalize the subgraphs
iLabels = []
for i in H_list_NoEmpty0:
    iLabelsItem = i.nodes(data=True)
    iLabels.append(iLabelsItem)
dictIlabels = [dict(i) for i in iLabels]
names0 = [list(natsorted(item.keys())) for item in dictIlabels]

namesNoNumber = [[re.sub(r'_(.*?)_', '', i) for i in sublist] for sublist in names0]
res = [[list(i) for j, i in itertools.groupby(natsorted(sublist))] for sublist in namesNoNumber] 
indexRes = [[[index[0] for index in enumerate(i)] for i in sublist] for sublist in res]
nameDictionary = [{a:c for a,c in zip(x,y)} for (x,y) in zip(names0,namesNoNumber)]

sortedd = []
for x in nameDictionary:
    d = {k: v for k, v in natsorted(x.items(), key=lambda item: item[1])}
    sortedd.append(d)

listItems = [list(i.items()) for i in sortedd]
flatIndexRes = [[item for subsublist in sublist for item in subsublist] for sublist in indexRes] 
finalZip = [[(a,b) for a,b in zip(x,y)] for x,y in zip(listItems,flatIndexRes)]
finalZip0 = [[(a,b+"_"+str(c)+"_") for (a,b), c in x] for x in finalZip]
newRenumberedDict = [{a:b for a,b in item} for item in finalZip0] 

RelabeledGraphs = []
for x,y in zip(H_list_NoEmpty0,newRenumberedDict):
    KK = nx.relabel_nodes(x, y)
    RelabeledGraphs.append(KK)
######re-indexing labels###### 

#to drop graphs with no edges
Final_NoEmpty = []
for x in RelabeledGraphs:  
    if x.number_of_edges() != 0:
        Final_NoEmpty.append(x)

print("Final subgraph partition:")

for i,sub in enumerate(Final_NoEmpty):
    print("Final_Subgraph_{}:".format(i),sub)
sub_len_no3 = [len(i.nodes()) for i in Final_NoEmpty]
print("partition total graph nodes no.: ", sum(sub_len_no3))
sub_len_edg3 = [len(i.edges()) for i in Final_NoEmpty]
print("partition total graph edges no.: ", sum(sub_len_edg3)) 
print("<---------------------------->")

dots = []
for i in Final_NoEmpty:
    dots.append(nx.drawing.nx_pydot.to_pydot(i))
dotsLs = [str(i).splitlines() for i in dots]

#NEW feature we added the directionality!!!!
filter0weight = [[re.sub(r'weight=', '', item) for item in sublist] for sublist in dotsLs]
filter1weight = [[re.sub(r', \d\]', ']', item) for item in sublist] for sublist in filter0weight]

r = re.compile('->')
filter0 = [[item for item in sublist if r.findall(item)] for sublist in filter1weight]
filter1 = [[re.sub(r'\n', '', item) for item in sublist] for sublist in filter0]
filter2 = [[re.sub(r'\[direction=""\]', '', item) for item in sublist] for sublist in filter1]
filter3 = [[re.sub(r'\;', '', item) for item in sublist] for sublist in filter2]
filter4 = [[re.sub(r'attribute=', '', item) for item in sublist] for sublist in filter3]
filter5 = [[re.sub(r'', '', item) for item in sublist] for sublist in filter4]
filter5_ = [[re.sub(r'\(', '', item) for item in sublist] for sublist in filter5]
filter5__ = [[re.sub(r'\)', '', item) for item in sublist] for sublist in filter5_]
filter5___ = [[re.sub(r'/', '', item) for item in sublist] for sublist in filter5__]
drop_empty = [ele for ele in filter5___ if ele != []]

# #CHECK falsifying CHAR!! TB
filter6 = [[re.sub(r',is', '-is', item) for item in sublist] for sublist in drop_empty]
ins = re.compile('^((?!instantiation@@).)*$') #- keep: @@
not_contain_in = [[item for item in sublist if ins.findall(item)] for sublist in filter6]
chrz = re.compile('^((?!characterization@@).)*$') #- keep: @@ 
not_contain_chrz = [[item for item in sublist if chrz.findall(item)] for sublist in not_contain_in]
filter7 = [[re.sub(r'->', ',->', item) for item in sublist] for sublist in not_contain_chrz]

#recover elements without indexes
n = re.compile('^((?!_(.*?)_).)*$')
not_contain = [[item for item in sublist if n.findall(item)] for sublist in filter7]
flatten_not = [val for sublist in not_contain for val in sublist]
final_not_sorted = not_contain_chrz+flatten_not
final = list(map(natsorted, final_not_sorted))

deriv = re.compile('^((?!derivation).)*$') 
not_contain_deriv = [[item for item in sublist if deriv.findall(item)] for sublist in final]
filter8 = [[re.sub(r'\._', '_', item) for item in sublist] for sublist in not_contain_deriv]

itemSetList = not_contain_deriv #if we want cardinalities, just keep "final"
graphGenerationEdges =  [[re.sub(r'->', ' -> ', item) for item in x] for x in itemSetList]
graphGenerationLabel =  [[re.sub(r'\[', ' [label=', item) for item in x] for x in graphGenerationEdges]
graphGenerationAtt =  [[re.sub(r'\]', ']', item) for item in x] for x in graphGenerationLabel]
graphGenerationAttClos =  [[item+";" for item in x] for x in graphGenerationAtt]
graphGenerationAttNull =  [[re.sub(r'ln', 'l-n', item) for item in x] for x in graphGenerationAttClos]
deleteKey = [[re.sub(r', key=\d', '', item) for item in x] for x in graphGenerationAttNull]
graphGenerationAttNull0 = ['\n'.join(i) for i in deleteKey]

path = "./subgraphs-single/{}".format(fileName+"_>="+str(partitionValue)+"Norm"+"_isaW_"+str(isaW)+"_relW_"+str(relW))
exist = os.path.isdir(path)
if not exist:
    new_dir = os.mkdir(path)
else:
    print("")

for i,graph in enumerate(graphGenerationAttNull0):
    f = open("{}/{}{}.txt".format(path,fileName,i), "w")
    f.write('digraph {\n')
    f.write('rankdir=BT;\n')
    f.write(graph)
    f.write('\n')
    f.write('}\n')
    f.close()

for i,graph in enumerate(graphGenerationAttNull0):
    f = open("./subgraphs-full/{}{}.txt".format(fileName,i), "w")
    f.write('digraph {\n')
    f.write('rankdir=BT;\n')
    f.write(graph)
    f.write('\n')
    f.write('}\n')
    f.close()

with open("./subgraphs-source/{}.txt".format(fileName), "w") as filehandle:
    for g in graphGenerationAttNull0:
        filehandle.write('%s\n' % g)

#visualization
import pygraphviz
from graphviz import Source
for r in os.listdir(path):
    if r.endswith('.txt'):
        f = os.path.join(path, r)
        g = nx.drawing.nx_agraph.read_dot(f)
        s = Source.from_file(f)
        s.render()
# %%

import time
start_time = time.time()
print("--- %s seconds ---" % (time.time() - start_time))