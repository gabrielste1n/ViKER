# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from enum import Enum
import numpy as np
from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM

path_write = '../Documentation/Phase 4/Generated/'

def EERToARM(filePath):
    # Produce a JSON representation of given schema in ARM
    entities = np.array(readEER(filePath)) # read in array of entities from JSON file
    strongEntities = np.array([E for E in entities if E.isStrong()])
    weakEntities = np.array([E for E in entities if not E.isStrong()])
    relations = np.array([])

    # Step 1: For each strong entity E, create a Relation T 
    #         Add regular Attributes to each T, Identify pathFD attributes 
    relations = np.concatenate([relations, StrongEntityToRelation(strongEntities)])

    # Step 2: for each weak entity W create a relation T
    #         Create pathFD from weak entity identifier + the related strong entity identifier
    relations = np.concatenate([relations, WeakEntityToRelation(weakEntities, strongEntities)])

    for E in strongEntities:
        alreadyProcessed = []
        for R in E.getRelationships():

            # Step 3: For each 1:1 relationship (only possible between two strong entities)
            #         Identify entities S and T participating in the relationship, select and 
            #         include in S as a foregin key, the primary key of T
            if ((R.getLocalRelationship() == RelationTypes.EXACTLY_ONE and 
                R.getForeignRelationship() == RelationTypes.EXACTLY_ONE) and not 
                (R.getEntityName() in alreadyProcessed)):

                oneToOneTransform(relations, R, E)
                

            # Step 4: For each 1:0...N relationship (only possible between two strong entities)
            #         Identify relations S->0..N, T->1. Include as a foreign key in S, the 
            #         primary key of T

            elif ((R.getLocalRelationship() == RelationTypes.ZERO_OR_MANY and 
                R.getForeignRelationship() == RelationTypes.EXACTLY_ONE) and not 
                (R.getEntityName() in alreadyProcessed)):

                manyToOneTransform(relations, R, E)

            # Step 5: For each M:N relationship (only possible between two strong entities)
            #         between relations S (local) and T (foreign) create a new relation R. 
            #         include as foreign key attributes the primary keys of S and T, 
            #         which will together form the primary key for R. 
            #         Also add any simple attributes belonging to the relationship to R.

            elif ((R.getLocalRelationship() == RelationTypes.ZERO_OR_MANY and 
                R.getForeignRelationship() == RelationTypes.ZERO_OR_MANY) and not 
                (R.getEntityName() in alreadyProcessed)):

                T = np.array(manyToManyTransform(relations, R, E))
                relations = np.concatenate(relations, T)

        alreadyProcessed.append(E.getName())

    writeARM(path_write+"arm.JSON", list(relations))

# def ARMToEER(self):
#     # Produce JSON representation of given schema in ER

# def produceOOP(self, file):
#     # Produce OOP representation of schema from given ARM or ER JSON file

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
    toReturn = []
    for W in weakEntities:
        # Create a new relation for each weak entity
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
            index = [x.getName() for x in strongEntities].index(R.entityName)
            ownerEntity = strongEntities[index]

            # Add each identifier attribute belonging to the owner entity as a foregn key attribute to the weak entity 
            for A in ownerEntity.getIDAttribs():
                T.addAttribute(
                       name=A.getName(), 
                       isConcrete=False, 
                       dataType=DataTypes.OID, 
                       isPFD=True, 
                       isFK=True,
                       FKPointer = A # A reference to the Attribute (Column in DB) 
                       )

        toReturn.append(T) # Add relation to list to be returned

    return np.array(toReturn)

def oneToOneTransform(relations, R, E):
    foreignRelationIndex = [x.getName() for x in relations].index(R.getEntityName()) # get the index of the relation corresponding to the foreign entity
    T = relations[foreignRelationIndex] # the relation corresponding to the foreign entity 

    # Add primary key attribute(s) to T corresponding to the identifier attributes in E 
    for A in E.getIDAttribs():
        T.addAttribute(
               name=A.getName(), 
               isConcrete=False, 
               dataType=DataTypes.OID, 
               isPFD=False, 
               isFK=True,
               FKPointer = A
               )

def manyToOneTransform(relations, R, E):
    foreignRelationIndex = [x.getName() for x in relations].index(R.getEntityName()) # get the index of the relation corresponding to the foreign entity
    T = relations[foreignRelationIndex] # the relation corresponding to the foreign entity
    # Add primary key attribute(s) to T corresponding to the identifier attributes in E 
    for A in E.getIDAttribs():
        T.addAttribute(
               name=A.getName(), 
               isConcrete=False, 
               dataType=DataTypes.OID, 
               isPFD=False, 
               isFK=True,
               FKPointer = A
               )

def manyToOneTransform(relations, R, LE):
    foreignEntityIndex = [x.getName() for x in strongEntities].index(R.getEntityName()) # get the index of the relation corresponding to the foreign entity
    FE = strongEntities[foreignEntityIndex] # the relation corresponding to the foreign entity

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

    for A in np.concatenate([LE.getIDAttribs(), FE.getIDAttribs]):
        T.addAttribute(
                       name=A.getName(), 
                       isConcrete=False, 
                       dataType=DataTypes.OID, 
                       isPFD=True, 
                       isFK=True,
                       FKPointer=A
                       )

    for Aname in R.getAttributes():
        T.addAttribute(
                       name=Aname, 
                       isConcrete=True, 
                       dataType=DataTypes.ANY_TYPE, 
                       isPFD=False, 
                       isFK=False
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