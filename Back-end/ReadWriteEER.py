# Read in and write EER JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import json
import Relationship
from Table import Entity
from Attribute import ERAttribute

def readEER(filename):
    '''Reads in JSON EER file and creates relevant objects as needed.'''
    with open(filename, 'r', encoding='utf8', errors='ignore', ) as json_file:
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

def writeEER(filename, entities):
    '''Writes JSON EER representation from OOP representation.'''

    json_entities = {}
    json_entities['entities'] = []

    for entitiy in entities:
        name = entitiy.getName()
        isStrong = entitiy.isStrong()
        
        attributes = []
        for attribute in entitiy['attributes']:
            attributeName = attribute.getName()
            isIdentifier = attribute.isIdentifier()
            isMultiValued = attribute.isMultiValued()
            composedOf = attribute.composedOf()

            attributes.append(
                {
                    "AttributeName": attributeName,
                    "isIdentifier": isIdentifier,
                    "isMultiValued": isMultiValued,
                    "composedOf": composedOf
                }
            )

        relationships = []
        for relationship in entitiy['relationships']:
            entity = relationship.getEntityName()
            relationTypeLocal = relationship.getLocalRelationship()
            relationTypeForeign = relationship.getForeignRelationship()
            relationAttributes = relationship.getAttributes()

            relationships.append(
                {
                    "Entity": entity,
                    "RelationTypeLocal": relationTypeLocal,
                    "RelationTypeForeign": relationTypeForeign,
                    "relationAttributes": relationAttributes
                }
            )


        json_entities['entities'].append(
            {
                "name": name,
                "isString": isStrong,
                "attributes": attributes,
                "relationships": relationships
            }
        )

    with open(filename, 'w', encoding='utf8', errors='ignore') as json_file:
        json.dump(json_entities, json_file, indent=4)
