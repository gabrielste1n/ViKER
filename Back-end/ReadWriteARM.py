# Read in and write ARM JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import json
from Table import Relation
from Attribute import ARMAttribute

def readARM(filename):
    '''Reads in JSON ARM file and creates relevant objects as needed.'''
    with open(filename, 'r') as json_file:
        relations = json.load(json_file)
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

def writeARM(filename, relations):
    '''Writes JSON ARM representation from OOP representation.'''

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

    with open(filename, 'w') as json_file:
        json.dump(json_relations, json_file, indent=4, sort_keys=True)
