# Read in and write ARM JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import json
from Table import Relation
from Attribute import ARMAttribute

def readARM(filename):
    '''Reads in JSON ARM file and creates relevant objects as needed.'''
    with open(filename, 'r', encoding='utf8', errors='ignore') as json_file:
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

def writeARM(filename):
    '''Writes JSON ARM representation from OOP representation.'''
    with open(filename, 'w', encoding='utf8', errors='ignore') as json_file:
        
