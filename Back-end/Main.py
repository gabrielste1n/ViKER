# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from enum import Enum
import numpy as np
from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM
from Table import Relation, Entity

path_write = '../Documentation/Phase 4/Generated/'

def EERToARM(filePathRead, filePathWrite):
    # Produce a JSON representation of given schema in ARM
    entities = np.array(readEER(filePathRead)) # read in array of entities from JSON file
    strongEntities = np.array([E for E in entities if E.isStrongEntity()])
    weakEntities = np.array([E for E in entities if not E.isStrongEntity()])
    relations = np.array([])

    # Step 1: 
    # For each strong entity E, create a Relation T Add regular Attributes to each T & 
    # Identify pathFD attributes 
    relations = np.concatenate([relations, StrongEntityToRelation(strongEntities)])

    # Step 2:
    # For each weak entity W create a relation T, Add regular Attributes to each T &
    # create pathFD from weak entity + related strong entity identifiers
    relations = np.concatenate([relations, WeakEntityToRelation(weakEntities, strongEntities)])

    alreadyProcessed = [] # store foreign entity references which have already been processed

    for E in strongEntities:
        for R in E.getRelationships():
            pair = sorted((E.getName(), R.getEntityName())) # tuple (local, foreign)

            # Step 3: 
            # For each 1:1 relationship (only possible between two strong entities)
            # Identify entities S and T participating in the relationship, select and 
            # include in S as a foregin key, the primary key of T
            if((R.getLocalRelationship() == RelationTypes.EXACTLY_ONE.value and 
                R.getForeignRelationship() == RelationTypes.EXACTLY_ONE.value) and not 
                pair in alreadyProcessed):

                oneToOneTransform(relations, R, E)
                alreadyProcessed.append(pair)
                

            # Step 4: 
            # For each 1:0...N relationship (only possible between two strong entities)
            # Identify relations S->0..N (local), T->1 (foreign). Include as a foreign key 
            # in S, the primary key of T
            elif((R.getLocalRelationship() == RelationTypes.ZERO_OR_MANY.value and 
                R.getForeignRelationship() == RelationTypes.EXACTLY_ONE.value)):

                foreignEntityIndex = [x.getName() for x in strongEntities].index(R.getEntityName()) 
                FE = strongEntities[foreignEntityIndex] # get foreign entity

                manyToOneTransform(relations, E, FE)

            # Step 5: 
            # For each M:N relationship (only possible between two strong entities)
            # between relations S (local) and T (foreign) create a new relation R. 
            # include as foreign key attributes the primary keys of S and T, which will 
            # together form the primary key for R. Also add any simple attributes belonging 
            # to the relationship to R.
            elif((R.getLocalRelationship() == RelationTypes.ZERO_OR_MANY.value and 
                R.getForeignRelationship() == RelationTypes.ZERO_OR_MANY.value) and not
                pair in alreadyProcessed):

                foreignEntityIndex = [x.getName() for x in strongEntities].index(R.getEntityName()) 
                FE = strongEntities[foreignEntityIndex] # get foreign entity

                T = np.array(manyToManyTransform(E, FE, R)) # create a new relation for the many-many relationship 
                relations = np.concatenate([relations, T])

                alreadyProcessed.append(pair)

    writeARM(filePathWrite, list(relations))

def ARMToEER(filePathRead, filePathWrite):
    # Produce JSON representation of given schema in EER
    relations = np.array(readARM(filePathRead)) # read in array of entities from JSON file

    entities = []
    weakRelationshipTypes = []
    StrongOrRegularRelationshipTypes = []

    for T in relations:
        # loop through all relations
        relationshipType = getRelationshipType(T) #

        if(relationshipType=="strong"):
            # If relationshipType == "strong" create a strong entity
            entities.append(createEntity(T, isStrong=True))
            StrongOrRegularRelationshipTypes.append(T)

        elif(relationshipType == "regular"):
            # If relationshipType == "regular" create a weak entity 
            entities.append(addEntity(T, isStrong=False))
            StrongOrRegularRelationshipTypes.append(T)

        else:
            # If relationshipType == "weak" do NOT create a new entity, rather let the attributes belong to the relationship
            weakRelationshipTypes.append(T)

        entities.append(E)

    for T in StrongOrRegularRelationshipTypes:
        CreateRegularRelationships(T, entities)

    for T in weakRelationshipTypes:
        createSpecialRelationships(T, entities)

    return entities

#############################################################################################
# ER -> ARM Functions
#############################################################################################
def StrongEntityToRelation(strongEntities):
    toReturn = [] 
    for E in strongEntities:
        # Create the relation that corresponds with the strong entity
        T = Relation(
                     name=E.name,
                     inheritsFrom="none", # TO BE UPDATED
                     )

        # Add the "self" reference 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=DataTypes.OID.value, 
                       isPFD=False,
                       isFK=False
                       )

        # Add all non-composite (simple) attributes
        for A in [x for x in E.attributes if len(x.composedOf) == 0]:
            T.addAttribute(
                           name=A.getName(), 
                           isConcrete=True,
                           dataType=DataTypes.ANY_TYPE.value, 
                           isPFD=A.isIdentifierAttribute(), 
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
                    )

        # Add the "self" reference 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=DataTypes.OID.value, 
                       isPFD=False, 
                       isFK=False
                       )

        # Add all non-composite (simple) attributes
        for A in [x for x in W.attributes if len(x.composedOf) == 0]:
            T.addAttribute(
                           name=A.getName(), 
                           isConcrete=True, 
                           dataType=DataTypes.ANY_TYPE.value, 
                           isPFD=A.isIdentifierAttribute(), 
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
                       dataType=DataTypes.OID.value, 
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
               dataType=DataTypes.OID.value, 
               isPFD=False, 
               isFK=True,
               FKPointer = A
               )

def manyToOneTransform(relations, E, FE):
    localRelationIndex = [x.getName() for x in relations].index(E.getName())
    T = relations[localRelationIndex] # the relation corresponding to the foreign entity (The many-side)

    # TO DO: If E has no ID attributes (but is obviously still strong) it is an associative entity
    # and it must have as it's primary key(s) the primary keys of each of it's related entitiys
    
    # Add as foreign keys (and PFDs) to the many-side relation the identifiers of the one-side entity (E)   
    for A in FE.getIDAttribs():
        T.addAttribute(
               name=A.getName(), 
               isConcrete=False, 
               dataType=DataTypes.OID.value, 
               isPFD=False, 
               isFK=True,
               FKPointer = A
               )

def manyToManyTransform(E, FE, R):
    

    # Create a new relation corresponding to the Manay-Many relationship
    T = Relation(
                name="joinRelation["+E.getName()+"-"+FE.getName()+"]",
                inheritsFrom="none", # TO BE UPDATED
                coveredBy=[], 
                disjointWith=[]
                )

    # Add the "self" reference 
    T.addAttribute(
                   name="self", 
                   isConcrete=False, 
                   dataType=DataTypes.OID.value, 
                   isPFD=False, 
                   isFK=False
                   )
    # Add regular attributes belonging to the relationship
    for Aname in R.getAttributes(): 
        T.addAttribute(
                        name=Aname, 
                        isConcrete=True, 
                        dataType=DataTypes.ANY_TYPE.value, 
                        isPFD=False, 
                        isFK=False 
                        )

    # Add ID attributes from local entity
    for A in E.getIDAttribs(): 
        T.addAttribute(
                        name=A.getName(), 
                        isConcrete=False, 
                        dataType=DataTypes.OID.value, 
                        isPFD=True, 
                        isFK=True
                        )

    # Add ID attributes from foreign entity
    for A in FE.getIDAttribs(): 
        T.addAttribute(
                        name=A.getName(), 
                        isConcrete=False, 
                        dataType=DataTypes.OID.value, 
                        isPFD=True, 
                        isFK=True
                        )

    return np.array([T])

#############################################################################################
# ARM -> ER Functions
#############################################################################################

def getRelationshipType(T):
    PFDs = [A for A in T.getAttributes() if A.isPFD()] # All attributes A1,..., An s.t. pathfd(A1,...An) -> self
    FKs = 0

    for A in PFDs:
        if(A.isFK()):
            FKs += 1 # An attribute is both a PFD and an FK

    if(FKs == len(PFDs)):
        # All PFD attributes are also foreign keys => weak entity (dependant)
        return "weak"

    elif(FKs == 0):
        # None of the PFD attributes are foreign keys => strong entity
        return "strong"

    else:
        # Some of the PFD attributes are foreign keys, but some are not => regular
        return "regular"

def createEntity(T, isStrong):
    """Add a strong entity"""
    # Create a new entity object, add regular attributes of T
    # Add attributes
    attributes = []
    for ARMattrib in T.getAttributes():
        if(ARMattrib.isConcrete()):
            # All non-OID attributes
            if(ARMattrib.isPFD()):
                # is identifier attribute
                ERAttrib = ERAttribute(name = ARMattrib.getName(), isIdentifier=True)
                attributes.append(ERAttrib)
            else:
                # is not identifier attribute
                ERAttrib = ERAttribute(name = ARMattrib.getName(), isIdentifier=False)
                attributes.append(ERAttrib)

    # create new entity object
    E = Entity(
               name = T.getName(), 
               isStrong = isStrong, 
               attributes = attributes 
              )

    return E

def createRegularRelationship(T, entities):
    # get local entity associated with T 
    localEntityIndex = [e.getName() for e in entities].index(T.getName())
    LE = entities[localEntityIndex]

    # get all foreign key names from relation T
    FKnames = [a.getName() for a in T.getAttributes() if a.isFK()]
    
    # for foreign entity E:
    # if the Identifiers of E are all in FKnames;
    # create a many (local) to one (foreign) relation   
    for FE in entities:
        IdAttribNames = [a.getName() for a in FE.getIDAttribs()]

        if(LE.getName() == FE.getName()):
            add == False
        else:
            add = True

        for a in IdAttribNames:
            if not a in FKnames:
                add = False
        if add:
            LE.addRelationship(
                               entityName = FE.getName(), 
                               relationshipTypeLocal = DataTypes.ZERO_OR_MANY.value, 
                               relationshipTypeForeign = DataTypes.EXACTLY_ONE
                               )

def createSpecialRelationships(T, entities):
    regularAttributes = [a for a in T.getAttributes() if not a.isFK()]
    FKAttributeNames = [a.getName() for a in T.getAttributes() if a.isFK()]
    associatedEntities = []

    for E in entities:
        for A in E.getIDAttribs():
            if((A.getName() in FKAttributeNames) and not E.getName() in associatedEntities):
                associatedEntities.append(E)

    E1 = associatedEntities[0]
    E2 = associatedEntities[1]

    E1.addRelationship(
                        entityName = E2, 
                        relationshipTypeLocal = DataTypes.ZERO_OR_MANY.value, 
                        relationshipTypeForeign = DataTypes.ZERO_OR_MANY.value, 
                        attributes = [a.getName() for a in regularAttributes]
                        )

    E2.addRelationship(
                        entityName = E1, 
                        relationshipTypeLocal = DataTypes.ZERO_OR_MANY.value, 
                        relationshipTypeForeign = DataTypes.ZERO_OR_MANY.value, 
                        attributes = [a.getName() for a in regularAttributes])

class DataTypes(Enum):
    '''Specific types of data available'''
    ANY_TYPE = 'AnyType'
    INTEGER = 'Integer'
    FLOAT = 'FloatingPoint'
    STRING = 'String'
    OID = 'OID'

class RelationTypes(Enum):
    '''Types of relationships between entities'''
    EXACTLY_ONE = 'ExactlyOne'
    ZERO_OR_MANY = 'ZeroOrMany'
    INHERITS_FROM = 'ISA'
    # ZERO_OR_ONE = 'ZeroOrOne'
    # ONE_OR_MORE = 'OneOrMore'
    # MANY = 'Many' 
