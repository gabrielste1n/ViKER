# Read in and write EER JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

import json
from Relationship import Relationship
from Table import Entity
from Attribute import ERAttribute

def readEER(entities):
    '''
    Reads in JSON EER file and creates relevant objects as needed
    
    Parameters
    ----------
    entities: a JSON file containing the structure of the entities in the ER model

    Returns
    -------
    toReturn: an array of entity objects
    '''

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

def writeEER(entities):
    '''
    Creates JSON EER representation from array of relation objects
    
    Parameters
    ----------
    entities: an array of relation objects 

    Returns 
    json_entities: a JSON file containing the structure of the entities in the EER model
    '''

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
    return json_entities

