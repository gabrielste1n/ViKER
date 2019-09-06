# Read in and write ARM JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

import json
from Table import Relation
from Attribute import ARMAttribute

def readARM(relations):
    '''
    Reads in JSON ARM file and creates relevant objects as needed
    
    Parameters
    ----------
    relations: a JSON file containing the structure of the relations in the AR model

    Returns
    -------
    toReturn: an array of relation objects
    '''
    toReturn = []
    for relation in relations['relations']:
        attributes = []
        for attribute in relation['attributes']:
            tempAttribute = ARMAttribute(
                attribute['AttributeName'],
                attribute['isConcrete'],
                attribute['dataType'],
                attribute['isPathFunctionalDependancy'],
                attribute['isFK']
            )
            attributes.append(tempAttribute)

        tempRelation = Relation(
            relation['name'],
            attributes,
            relation['inheritsFrom'],
            relation['coveredBy'],
            relation['disjointWith']
        )
        toReturn.append(tempRelation)
            
    return toReturn

def writeARM(relations):

    '''
    Creates JSON ARM representation from array of relation objects
    
    Parameters
    ----------
    relations: an array of relation objects 

    Returns 
    json_relations: a JSON file containing the structure of the relations in the AR model
    '''

    json_relations = {}
    json_relations['relations'] = []

    for relation in relations:
        name = relation.getName()
        inheritsFrom = relation.getInheritsFrom()
        coveredBy = relation.getCoveredBy()
        disjointWith = relation.getDisjointWith()

        attributes = []
        for attribute in relation.attributes:
            attributeName = attribute.getName()
            isConcrete = attribute.isConcreteAttribute()
            dataType = attribute.getDataType()
            isPathFunctionalDependency = attribute.isPathFunctionalDependency()
            isForeignKey = attribute.isForeignKey()

            attributes.append(
                {
                    "AttributeName": attributeName,
                    "isConcrete": isConcrete,
                    "dataType": dataType,
                    "isPathFunctionalDependancy": isPathFunctionalDependency,
                    "isFK": isForeignKey
                }
            )

        json_relations['relations'].append(
            {
                "name": name,
                "attributes": attributes,
                "inheritsFrom": inheritsFrom,
                "coveredBy": coveredBy,
                "disjointWith": disjointWith
            }
        )

    return json_relations
