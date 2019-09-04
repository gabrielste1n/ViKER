# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from enum import Enum
import numpy as np
from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM
from Table import Relation, Entity

#############################################################################################
# ARM -> ER Functions
#############################################################################################
def ARMToEER(filePathRead, filePathWrite):
    # Produce JSON representation of given schema in EER
    relations = np.array(readARM(filePathRead)) # read in array of entities from JSON file

    entities = []
    weakRelationTypes = []
    StrongOrRegularRelationTypes = []

    for T in relations:
        # loop through all relations
        relationType = getRelationshipType(T) #

        if(relationType=="strong"):
            # If relationType == "strong" create a strong entity 
            entities.append(createEntity(T, isStrong=True))
            StrongOrRegularRelationTypes.append(T)
 
        elif(relationType == "regular"):
            # If relationType == "regular" create a weak entity 
            entities.append(createEntity(T, isStrong=False))
            StrongOrRegularRelationTypes.append(T)

        elif(relationType == 'weak'):
            # If relationType == "weak" do NOT create a new entity, rather let the attributes belong to the relationship (alternatively this could be an associative relationship)
            weakRelationTypes.append(T)

        elif(relationType == 'isa'):
            # If relationshipType == 'isa' create a weak entity that inherits from a super-entity 
            entities.append(createISAEntity(T, entities))

    for T in StrongOrRegularRelationTypes:
        createRegularRelationships(T, entities)

    for T in weakRelationTypes:
        createAttributeRelationships(T, entities)

    writeEER(filePathWrite, list(entities))

def getRelationshipType(T):
    PFDs = [A for A in T.getAttributes() if A.isPathFunctionalDependency()] # All attributes A1,..., An s.t. pathfd(A1,...An) -> self
    FKs = 0

    for A in PFDs:
        if(A.isForeignKey()):
            FKs += 1 # An attribute is both a PFD and an FK

    if(FKs == len(PFDs)):
        # All PFD attributes are also foreign keys => weak entity (dependant)
        if(T.getInheritsFrom() == "none"):
            return "weak"
        else:
            return "isa"

    elif(FKs == 0):
        # None of the PFD attributes are foreign keys => strong entity
        return "strong"

    else:
        # Some of the PFD attributes are foreign keys, but some are not => regular
        return "regular"

def createEntity(T, isStrong):
    """Add a strong entity"""
    # Create a new entity object, add regular attributes of T
    
    # create new entity object
    E = Entity(
               name = T.getName(), 
               isStrong = isStrong
               )

    # Add attributes
    for ARMattrib in T.getAttributes():
        if(ARMattrib.isConcreteAttribute()):
            # All non-OID attributes
            if(ARMattrib.isPathFunctionalDependency()):
                # is identifier attribute
                E.addAttribute(
                               name = ARMattrib.getName(), 
                               isIdentifier=True
                              )
            else:
                # is not identifier attribute
                E.addAttribute(
                               name = ARMattrib.getName(), 
                               isIdentifier=False
                              )
    return E

def createISAEntity(T, entities):
    # create new entity object
    subEntity = Entity(
                       name = T.getName(), 
                       isStrong = False
                      )

    for A in T.getAttributes():
        if((not A.isForeignKey()) and (A.isConcreteAttribute()))  :
            subEntity.addAttribute(
                                   name=A.getName(), 
                                   isIdentifier=False, 
                                  )

    superEntityName = T.getInheritsFrom()
    for E in entities:
        if(E.getName() == superEntityName):
            superEntity = E
            break

    subEntity.addRelationship(
                              entityName = superEntity.getName(), 
                              relationshipTypeLocal = RelationTypes.INHERITS_FROM.value, 
                              relationshipTypeForeign = RelationTypes.INHERITS_FROM.value, 
                              attributes=None
                              )

    superEntity.addRelationship(
                                entityName = subEntity.getName(), 
                                relationshipTypeLocal = RelationTypes.INHERITS_FROM.value, 
                                relationshipTypeForeign = RelationTypes.INHERITS_FROM.value, 
                                attributes=None
                               )

    return subEntity

def createRegularRelationships(T, entities):
    # get local entity associated with T 
    localEntityIndex = [e.getName() for e in entities].index(T.getName())
    LE = entities[localEntityIndex]

    # Names of all foreign key attributes of local relation
    FKnames = [a.getName() for a in T.getAttributes() if a.isForeignKey()] 
    
    for FE in entities:

        # Check that each Id attribute of the foreign entity is present in 
        # the list of foreign keys belonging to the local entity
        foreignIdAttribs = FE.getIDAttribs()
        if(len(foreignIdAttribs) == 0):
            continue

        for foreignIdAttrib in foreignIdAttribs:
            add = True
            if((foreignIdAttrib.getName() not in FKnames)):
                add = False

        # If the foreign entity is the same as the local entity
        if((FE.getName == LE.getName) and add):
            # A recursive relationship - TBC
            continue

        # If the foreign entity is not the same as the local entity
        # add a many to one relationship between the LE (many) and FE (one)
        elif((FE.getName() != LE.getName()) and add):
            FE.addRelationship(
                               entityName = LE.getName(), 
                               relationshipTypeLocal = RelationTypes.EXACTLY_ONE.value, 
                               relationshipTypeForeign = RelationTypes.ZERO_OR_MANY.value
                               )

            LE.addRelationship(
                               entityName = FE.getName(), 
                               relationshipTypeLocal = RelationTypes.ZERO_OR_MANY.value, 
                               relationshipTypeForeign = RelationTypes.EXACTLY_ONE.value
                               )

def createAttributeRelationships(T, entities):
    """Create a relationship with regular attributes from the weak Relation"""
    regularAttributes = [a.getName() for a in T.getAttributes() 
                         if (not a.isForeignKey()) 
                         and (a.isConcreteAttribute())]
    FKAttributeNames = [a.getName() for a in T.getAttributes() if a.isForeignKey()]
    relatedEntities = []
    
    for E in entities:
        # Find both entities referefnce in the foreign key list of the Relation
        for A in E.getIDAttribs():
            add = True
            if(not A.getName() in FKAttributeNames):
                add = False
            if(add and not E.getName() in relatedEntities):
                # Add a many (local) to many (foreign) relationship to the entity
                relatedEntities.append(E)

    if(len(relatedEntities) == 2):
        relatedEntities[0].addRelationship(
                                           entityName = relatedEntities[1].getName(), 
                                           relationshipTypeLocal = RelationTypes.ZERO_OR_MANY.value, 
                                           relationshipTypeForeign = RelationTypes.ZERO_OR_MANY.value, 
                                           attributes = regularAttributes
                                           )
        relatedEntities[1].addRelationship(
                                           entityName = relatedEntities[0].getName(), 
                                           relationshipTypeLocal = RelationTypes.ZERO_OR_MANY.value, 
                                           relationshipTypeForeign = RelationTypes.ZERO_OR_MANY.value, 
                                           attributes = regularAttributes
                                           )

#############################################################################################
# ER -> ARM Functions
#############################################################################################
def EERToARM(filePathRead, filePathWrite):
    # Produce a JSON representation of given schema in ARM
    entities = np.array(readEER(filePathRead)) # read in array of entities from JSON file
    strongEntities = np.array([E for E in entities if E.isStrongEntity()])
    weakEntities = np.array([E for E in entities if not E.isStrongEntity()])
    PFDMap = {}
    relations = np.array([])

    # Step 1: 
    # For each strong entity E, create a Relation T Add regular Attributes to each T & 
    # Identify pathFD attributes 
    T = StrongEntityToRelation(strongEntities)
    relations = np.concatenate([relations, T])

    # Step 2:
    # For each weak entity W create a relation T, Add regular Attributes to each T &
    # create pathFD from weak entity + related strong entity identifiers
    T = WeakEntityToRelation(weakEntities, strongEntities)
    relations = np.concatenate([relations, T])

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
                manyToOneTransform(E, FE, relations)

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

    # Store pathFD references in pathFD map
    for relation in relations: 
        key = relation.getName() + "_" +str(hex(id(relation)))
        PFDMap[key] = (hex(id(a))  for a in relation.getAttributes() if a.isPathFunctionalDependency())

    writeARM(filePathWrite, list(relations))

def StrongEntityToRelation(strongEntities):
    toReturn = [] 
    multivaluedAttributes = []

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
            if(A.isMultiValuedAttribute()):
                multivaluedAttributes.append(A)
            else:
                T.addAttribute(
                               name=A.getName(), 
                               isConcrete=True,
                               dataType=DataTypes.ANY_TYPE.value, 
                               isPFD=A.isIdentifierAttribute(), 
                               isFK=False
                               )

        toReturn.append(T) # append relation to list to be returned

        for multivaluedAttribute in multivaluedAttributes:
            T = multivaluedToRelation(multivaluedAttribute, E.getIDAttribs())
            toReturn.append(T)

    return np.array(toReturn) # return list of relations

def WeakEntityToRelation(weakEntities, strongEntities):
    toReturn = []
    for W in weakEntities:
        # Create a new relation for each weak entity

        inheritsFrom = "none"

        for r in W.getRelationships():
            if(r.getForeignRelationship() == RelationTypes.INHERITS_FROM.value):
                inheritsFrom = r.getEntityName()

        T = Relation(
                    name=W.getName(),
                    inheritsFrom=inheritsFrom,
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

def multivaluedToRelation(attribute, FKAttributes):
    # Create the relation that corresponds with the strong entity
        T = Relation(
                     name=attribute.getName(),
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

        # Add ID attribute 
        T.addAttribute(
                       name=attribute.getName()+"ID", 
                       isConcrete=True, 
                       dataType=DataTypes.ANY_TYPE.value, 
                       isPFD=True,
                       isFK=False
                       )

        for FKAttrib in FKAttributes:
            T.addAttribute(
                       name=FKAttrib.getName(), 
                       isConcrete=False, 
                       dataType=DataTypes.OID.value, 
                       isPFD=True,
                       isFK=True
                       )
        return T

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

def manyToOneTransform(E, FE, relations):
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
    ONE_OR_MORE = 'OneOrMore'
    # MANY = 'Many' 
    # ZERO_OR_ONE = 'ZeroOrOne'

