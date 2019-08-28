# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from enum import Enum
import numpy as np
# from ReadWriteEER import readEER

'''Driver class for the ViKER Back-end implementation.'''
def EERToARM(filePath):
    # Produce a JSON representation of given schema in ARM
    #entities = np.array(readEER(filePath)) # read in array of entities from JSON file
    strongEntities = np.array([E for E in entities if E.isStrong()])
    weakEntities = np.array([E for E in entities if not E.isStrong()])
    Relations = np.array([])

    # Step 1: For each strong entity E, create a Relation T 
    #         Add regular Attributes to each T, Identify pathFD attributes 
    Relations = np.concatenate([
                                Relations, 
                                StrongEntityToRelation(strongEntities)
                                ])

    # Step 2: for each weak entity W create a relation T
    #         Create pathFD from weak entity identifier + the related strong entity identifier
    Relations = np.concatenate([
                                Relations, 
                                WeakEntityToRelation(weakEntities, strongEntities)
                                ])

def ARMToEER(self):
    # Produce JSON representation of given schema in ER

def produceOOP(self, file):
    # Produce OOP representation of schema from given ARM or ER JSON file

def StrongEntityToRelation(strongEntities):
    toReturn = [] 

    for E in strongEntities:
        # Create the relation that corresponds with the strong entity
        T = Relation(
                    name=E.name,
                    inheritsFrom="none", # TO BE UPDATED
                    coveredBy=[], 
                    disjointWith=[]
                    )

        # Add the "self" reference 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=DataTypes.ANY_TYPE, 
                       isPFD=A.isIdentifier, 
                       isFK=False
                       )

        # Add all non-composite (simple) attributes
        for A in [x for x in E.attributes if len(x.composedOf) == 0]:
            T.addAttribute(
                           name=A.getName(), 
                           isConcrete=True, 
                           dataType=DataTypes.ANY_TYPE, 
                           isPFD=A.isIdentifier(), 
                           isFK=False
                           )

        toReturn.append(T) # append relation to list to be returned

    return np.array(toReturn) # return list of relations

def WeakEntityToRelation(weakEntities, strongEntities):
    for W in weakEntities:
        T = Relation(
                    name=W.getName(),
                    inheritsFrom="none", # TO BE UPDATED
                    coveredBy=[], 
                    disjointWith=[]
                    )

        # Add the "self" reference 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=DataTypes.ANY_TYPE, 
                       isPFD=False, 
                       isFK=False
                       )

        # Add all non-composite (simple) attributes
        for A in [x for x in E.attributes if len(x.composedOf) == 0]:
            T.addAttribute(
                           name=A.getName(), 
                           isConcrete=True, 
                           dataType=DataTypes.ANY_TYPE, 
                           isPFD=A.isIdentifier(), 
                           isFK=False
                           )

        for R in W.getRelationships():
            # Loop through each relationship W has with other entities
            ownerEntityName = R.entityName
            index = [i for i, x in enumnerate(strongEntities) if x.getName() == ownerEntityName]
            ownerEntity = strongEntities[index]
            for A in ownerEntity.getIDAttribs():
                T.addAttribute(
                       name=A.getName(), 
                       isConcrete=True, 
                       dataType=DataTypes.ANY_TYPE, 
                       isPFD=True, 
                       isFK=True
                       )

class DataTypes(Enum):
    '''Specific types of data available'''
    ANY_TYPE = 'AnyType'
    INTEGER = 'Integer'
    FLOAT = 'FloatingPoint'
    STRING = 'String'
    OID = 'OID'

class RelationTypes(Enum):
    '''Types of relationships between entities'''
    ZERO_OR_MANY = 'ZeroOrMany'
    ZERO_OR_ONE = 'ZeroOrOne'
    EXACTLY_ONE = 'ExactlyOne'
    ONE_OR_MORE = 'OneOrMore'
    MANY = 'Many' 