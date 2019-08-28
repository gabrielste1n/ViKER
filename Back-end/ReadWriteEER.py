# Read in and write EER JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import json
from Relationship import Relationship
from Table import Entity
from Attribute import ERAttribute

def readEER(filename):
    '''Reads in JSON EER file and creates relevant objects as needed.'''
    with open(filename, 'r') as json_file:
        entities = json.load(json_file)
        toReturn = []
        for entity in entities['entities']:
            attributes = []
            for attribute in entity['attributes']:
                tempAttribute = ERAttribute(
                    attribute['AttributeName'],
                    attribute['isIdentifier'],
                    attribute['isMultiValued'],
                    attribute['composedOf']
                )
                attributes.append(tempAttribute)

            relationships = []
            for relationship in entity['relationships']:
                tempRelationship = Relationship(
                    relationship['Entity'],
                    relationship['RelationTypeLocal'],
                    relationship['RelationTypeForeign'],
                    relationship['relationAttributes']
                )
                relationships.append(tempRelationship)

            tempEntity = Entity(
                entity['name'],
                entity['isStrong'],
                attributes,
                relationships
            )
            toReturn.append(tempEntity)
                
        return toReturn

def writeEER(filename, entities):
    '''Writes JSON EER representation from OOP representation.'''

    json_entities = {}
    json_entities['entities'] = []

    for entity in entities:
        name = entity.getName()
        isStrong = entity.isStrongEntity()
        
        attributes = []
        for attribute in entity.getAttributes():
            attributeName = attribute.getName()
            isIdentifier = attribute.isIdentifierAttribute()
            isMultiValued = attribute.isMultiValuedAttribute()
            composedOf = attribute.getAttributeComposedOf()

            attributes.append(
                {
                    "AttributeName": attributeName,
                    "isIdentifier": isIdentifier,
                    "isMultiValued": isMultiValued,
                    "composedOf": composedOf
                }
            )

        relationships = []

        for relationship in entity.getRelationships():
            entityName = relationship.getEntityName()
            relationTypeLocal = relationship.getLocalRelationship()
            relationTypeForeign = relationship.getForeignRelationship()
            relationAttributes = relationship.getAttributes()

            relationships.append(
                {
                    "Entity": entityName,
                    "RelationTypeLocal": relationTypeLocal,
                    "RelationTypeForeign": relationTypeForeign,
                    "relationAttributes": relationAttributes
                }
            )

        json_entities['entities'].append(
            {
                "name": name,
                "isStrong": isStrong,
                "attributes": attributes,
                "relationships": relationships
            }
        )

    with open(filename, 'w') as json_file:
        json.dump(json_entities, json_file, indent=4, sort_keys=True)
