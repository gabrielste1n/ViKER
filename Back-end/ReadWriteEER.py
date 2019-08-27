# Read in and write EER JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import json
import Relationship
from Table import Entity
from Attribute import ERAttribute

def read(filename):
    '''Reads in JSON EER file and creates relevant objects as needed.'''
    with open(filename, 'r', encoding='utf8', errors='ignore') as json_file:
        entities = json.load(json_file)
        toReturn = []
        for entity in entities['relations']:
            attributes = []
            for attribute in entities['attributes']:
                tempAttribute = ERAttribute(
                    attribute['AttributeName'],
                    attribute['isIdentifier'],
                    attribute['isMultiValued'],
                    attribute['composedOf']
                )
                attributes.append(tempAttribute)

            relationships = []
            for relationship in entities['relationships']:

                # Check with Jeremy about Relationship class 
                # not having both entities and attributes

                tempRelationship = Relationship(
                    relationship['RelationType'],
                    relationship['Entity1'],
                    relationship['Entity2'],
                    relationship['relationAttributes'],
                )

            tempRelation = Entity(
                entities['name'],
                entities['isStrong'],
                attributes,
                relationships
            )
            toReturn.append(tempRelation)
                
        return toReturn

#def write():