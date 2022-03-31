import json
from scraping.jextractor import extract_element_from_json
from scraping.extract import json_extract
from itertools import chain
#from application.app.folder.file import func_name

def ontoUMLjsonA(z):
    with open(z, encoding="cp860") as f: #works with json exporter 0.3.0
        inputJson = json.load(f)
    ids = []  
    for i in extract_element_from_json(inputJson, ["model","contents","contents","id"]):
        ids.append(str(i).replace(".","A"))   
    names = []
    for i in extract_element_from_json(inputJson, ["model","contents","contents","name"]):
        names.append(str(i))
    stereotypes = []
    for i in extract_element_from_json(inputJson, ["model","contents","contents","stereotype"]):
        stereotypes.append(str(i))
    
    types = []
    for i in extract_element_from_json(inputJson, ["model","contents","contents","type"]):
        types.append(str(i))
    typesList = [x for x in zip(ids,names,stereotypes,types)]

    classTypes = []
    for i in typesList:
        if i[3] == 'Class':
            classTypes.append(i)

    finalClass = [(str(a),str(b),str(c)) for (a,b,c,d) in classTypes]
    
####

    generalIds = []  
    for i in extract_element_from_json(inputJson, ["model","contents","contents","general","id"]):
        generalIds.append(str(i).replace(".","A"))
    specificIds = []  
    for i in extract_element_from_json(inputJson, ["model","contents","contents","specific","id"]):
        specificIds.append(str(i).replace(".","A"))

    generalizationEdges = [x for x in zip(generalIds,specificIds)]
    filteredGenEdges = [item for item in generalizationEdges if 'None' not in item]

    genTypes = []
    for i in typesList:
        if i[3] == 'Generalization':
            genTypes.append(i)
    
    filteredGenTypes = [(a) for (a,b,c,d) in genTypes]
    finalGen = [(str(x),str(y),str(z)) for ((x,y),z) in zip(filteredGenEdges,filteredGenTypes)]

####
    existingCardinalities0 = []
    for x in inputJson["model"]['contents']:
        try:
            for y in x['contents']:
                if y['type'] == 'Relation':
                    existingCardinalities0.append(json_extract(y,"cardinality"))
        except KeyError:
            pass
        except TypeError:
            pass
    
    existingCardinalities = []
    for i in existingCardinalities0:
        existingCardinalities.append(tuple(i))
   
    pairedIds0 = []
    for x in inputJson["model"]['contents']:
        try:
            for y in x['contents']:
                if y['type'] == 'Relation':
                    couple = []
                    pairedIds0.append(couple)
                    for z in y['properties']:
                        couple.append(json_extract(z['propertyType'],"id"))
        except KeyError:
            pass
        except TypeError:
            pass
    
    pairedIds = []
    for i in pairedIds0:
        flat_list = [item for sublist in i for item in sublist]
        pairedIds.append(tuple(flat_list))
    
    cardAndIds = [i for i in list(zip(existingCardinalities,pairedIds))]
    cardAndIdsFlat = [tuple(chain.from_iterable(i))for i in cardAndIds]
    #print(len(cardAndIdsFlat))

    assoTypes = []
    for i in typesList:
        if i[3] == 'Relation':
            assoTypes.append(i)
            
    fullAsso = [i for i in list(zip(assoTypes,cardAndIdsFlat))]
    assIdsFlat_ = [tuple(chain.from_iterable(i))for i in fullAsso]
 
    
    assIdsFlat = []
    for x in assIdsFlat_:
        if len(x) == 8:
            assIdsFlat.append(x)
    
    finalAsso = [(str(g),str(h),str(a),str(e),str(f),str(c)) for (a,b,c,d,e,f,g,h) in assIdsFlat]
   
    return finalClass, finalAsso, finalGen

def ontoUMLjsonB(z):
    with open(z,encoding="cp860") as f: #works with json exporter 0.3.0
        inputJson = json.load(f)
    ids = []  
    for i in extract_element_from_json(inputJson, ["model","contents","id"]):
        ids.append(str(i).replace(".","A"))   
    names = []
    for i in extract_element_from_json(inputJson, ["model","contents","name"]):
        names.append(str(i))
    stereotypes = []
    for i in extract_element_from_json(inputJson, ["model","contents","stereotype"]):
        stereotypes.append(str(i))
    
    types = []
    for i in extract_element_from_json(inputJson, ["model","contents","type"]):
        types.append(str(i))
    typesList = [x for x in zip(ids,names,stereotypes,types)]

    classTypes = []
    for i in typesList:
        if i[3] == 'Class':
            classTypes.append(i)

    finalClass = [(str(a),str(b),str(c)) for (a,b,c,d) in classTypes]

####

    generalIds = []  
    for i in extract_element_from_json(inputJson, ["model","contents","general","id"]):
        generalIds.append(str(i).replace(".","A"))
    specificIds = []  
    for i in extract_element_from_json(inputJson, ["model","contents","specific","id"]):
        specificIds.append(str(i).replace(".","A"))

    generalizationEdges = [x for x in zip(generalIds,specificIds)]
    filteredGenEdges = [item for item in generalizationEdges if 'None' not in item]

    genTypes = []
    for i in typesList:
        if i[3] == 'Generalization':
            genTypes.append(i)
    
    filteredGenTypes = [(a) for (a,b,c,d) in genTypes]
    finalGen = [(str(x),str(y),str(z)) for ((x,y),z) in zip(filteredGenEdges,filteredGenTypes)]

####
    existingCardinalities0 = []
    for x in inputJson["model"]['contents']:
        try:
            if x['type'] == 'Relation':
                existingCardinalities0.append(json_extract(x,"cardinality"))
        except KeyError:
            pass
        except TypeError:
            pass
        
    existingCardinalities = []
    for i in existingCardinalities0:
        existingCardinalities.append(tuple(i))

    pairedIds0 = []
    for x in inputJson["model"]['contents']:
        try:
            if x['type'] == 'Relation':
                couple = []
                pairedIds0.append(couple)
                for z in x['properties']:
                    couple.append(json_extract(z['propertyType'],"id"))
        except KeyError:
            pass
        except TypeError:
            pass

    pairedIds = []
    for i in pairedIds0:
        flat_list = [item for sublist in i for item in sublist]
        pairedIds.append(tuple(flat_list))

    cardAndIds = [i for i in list(zip(existingCardinalities,pairedIds))]
    cardAndIdsFlat = [tuple(chain.from_iterable(i))for i in cardAndIds]

    assoTypes = []
    for i in typesList:
        if i[3] == 'Relation':
            assoTypes.append(i)
    

    fullAsso = [i for i in list(zip(assoTypes,cardAndIdsFlat))]
    assIdsFlat_ = [tuple(chain.from_iterable(i))for i in fullAsso]
    
    assIdsFlat = []
    for x in assIdsFlat_:
        if len(x) == 8:
            assIdsFlat.append(x)
    
    finalAsso = [(str(g),str(h),str(a),str(e),str(f),str(c)) for (a,b,c,d,e,f,g,h) in assIdsFlat]

    return finalClass, finalAsso, finalGen