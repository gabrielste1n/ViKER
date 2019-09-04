# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0
from enum import Enum
import numpy as np
from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM
from Table import Relation, Entity
import json

#############################################################################################
# ARM -> ER Functions
#############################################################################################
def ARMToEER(relations):
    """
    Given a JSON representation of an ARM schema, transform and produce a JSON 
    representation of the schema as an EER model.

    Parameters
    ----------
    relations: a dictionary containing the ARM schema data 

    filePathWrite: the directory where the JSON file output must be written to

    Returns
    -------
    entities: an array of entity objects representing the resultanting from
              the transformation. 
    """

    # Get an array of relation objects belonging to the ARM
    relations = np.array(readARM(relations)) 

    entities = [] # array for output entity objects

    # Sorting arrays for different catagories of relation objects
    weakRelationTypes = []
    StrongOrRegularRelationTypes = []

    # loop through all relation objects
    for T in relations:

        # A relation type can be strong, regular or weak (see function)
        relationType = getRelationshipType(T)

        if(relationType=="strong"):
            # If relationType is "strong" create a strong entity 
            entities.append(createEntity(T, isStrong=True))
            StrongOrRegularRelationTypes.append(T)
 
        elif(relationType == "regular"):
            # If relationType is "regular" create a weak entity 
            entities.append(createEntity(T, isStrong=False))
            StrongOrRegularRelationTypes.append(T)

        elif(relationType == 'weak'):
            # If relationType is "weak" do NOT create a new entity, rather let the attributes 
            # be assigned to the relationship between the entities on either side 
            weakRelationTypes.append(T)

        elif(relationType == 'isa'):
            # If relationshipType is 'isa' create a weak entity that inherits from (has an 
            # ISA relationship with) a super-entity 
            entities.append(createISAEntity(T, entities))

    # for each entity object created from a relation object catagorised as having a "strong" 
    # or "regular" type, create relationships based off foreign key attributes 
    for T in StrongOrRegularRelationTypes:
        createManyToOneRelationship(T, entities)

    # for each entity object created from a relation object catagorised as having a "weak" type, 
    # transform the relation into a many to many relationship between two associated entities
    for T in weakRelationTypes:
        createManyToManyRelationship(T, entities)

    # Write resultant entities to file
    return writeEER(list(entities))


def getRelationshipType(T):
    """
    Takes as argument a relation object and catagorises it as:

    Strong:  None of the attributes A1,...,An such that pathfd(A1,...,An) -> self
             are foreign keys

    Regular: Some of the attributes A1,...,Ak such that pathfd(A1,...Ak,Ak+1,...,An)->self
             are foreign keys

    Weak:    All of the attributes A1,...,An such that pathfd(A1,...,An) -> self
             are foreign keys

    Parameters
    ----------
    T: a relation object

    Returns
    -------
    String object ("weak", "regular" or "strong")
    """

    # Select all attributes A1,..., An such that pathfd(A1,...An) -> self
    PFDs = [A for A in T.getAttributes() if A.isPathFunctionalDependency()] 
    FKs = 0

    for A in PFDs:
        # If an attribute forms path of the pathFD and is also a foreign key
        if(A.isForeignKey()):
            FKs += 1 

    if(FKs == len(PFDs)):
        # All PFD attributes are also foreign keys, then either:
        if(T.getInheritsFrom() != "none"):
            # The relation is part of an inheritence hierachy (a subsumption relationship)
            return "isa"
        else:
            # The relation type is "weak" 
            return "weak"

    elif(FKs == 0):
        # None of the PFD attributes are foreign keys => the relation type is strong
        return "strong"

    else:
        # Some of the PFD attributes are foreign keys, but some are not => the relation
        # type is regular
        return "regular"

def createEntity(T, isStrong):
    """
    Create a new strong entity object.

    Parameters
    ----------
    T: Associated relation object from which to construct the entity

    isStrong: a boolean value indicating whether or not the entity is strong or not

    Returns
    -------
    E: Entity object

    """

    # create new entity object
    E = Entity(name = T.getName(), isStrong = isStrong)

    # Add attributes to entity object
    for ARMattrib in T.getAttributes():

        # If an attribute is concrete
        if(ARMattrib.isConcreteAttribute()):

            # is identifier attribute
            if(ARMattrib.isPathFunctionalDependency()):

                E.addAttribute(name = ARMattrib.getName(), isIdentifier=True)

            # is not identifier attribute
            else:
                E.addAttribute(name = ARMattrib.getName(), isIdentifier=False)
    
    return E

def createISAEntity(T, entities):
    """
    Given a relation object, create the corresponding entity object 
    which has a subsumption relatioship to a parent entity.

    Parameters
    ----------
    T: relation object

    entities: array of existing entity objects

    Returns
    -------
    subEntity: the new (child) entity object
    """
    # create new entity object
    subEntity = Entity(name = T.getName(), isStrong = False)

    # add all concrete attributes which are not foreign keys
    for A in T.getAttributes():
        if(not A.isForeignKey() and A.isConcreteAttribute()):
            subEntity.addAttribute(name=A.getName(), isIdentifier=False)

    # Find the parent entity
    superEntityName = T.getInheritsFrom()
    for E in entities:
        if(E.getName() == superEntityName):
            superEntity = E
            break

    # Add ISA relationship to child entity 
    subEntity.addRelationship(
                              entityName = superEntity.getName(), 
                              relationshipTypeLocal = RelationTypes.INHERITS_FROM.value, 
                              relationshipTypeForeign = RelationTypes.INHERITS_FROM.value
                             )

    # Add ISA relationship to parent entity
    superEntity.addRelationship(
                                entityName = subEntity.getName(), 
                                relationshipTypeLocal = RelationTypes.INHERITS_FROM.value, 
                                relationshipTypeForeign = RelationTypes.INHERITS_FROM.value, 
                               )

    # return new child entity
    return subEntity

def createManyToOneRelationship(T, entities):
    """
    Given a relation object, add the 1:N relationships based on the 
    foreign keys to the associated local and foreign entities.

    Parameters
    ----------
    T: relation object

    entities: array of existing entity objects

    Returns
    -------
    NoneType
    """

    # get local entity associated with T 
    localEntityIndex = [e.getName() for e in entities].index(T.getName())
    LE = entities[localEntityIndex]

    # Get the names of all foreign key attributes belonging to the relation
    FKnames = [a.getName() for a in T.getAttributes() if a.isForeignKey()] 
    
    # For each foreign entity in existing entities
    for FE in entities:

        # Get all identifier attributes beloning to the foreign entity
        foreignIdAttribs = FE.getIDAttribs()

        # If the foreign entity has no idenitifier attributes; continue (next loop)
        if(len(foreignIdAttribs) == 0): continue

        # Check whether all foreign entity ID attributes are also foreign keys of the local entity
        for foreignIdAttrib in foreignIdAttribs:
            add = True
            if((foreignIdAttrib.getName() not in FKnames)):
                add = False

        # If the foreign entity is the same as the local entity; continue (next loop)
        if((FE.getName == LE.getName) and add):
            # A recursive relationship - CANNOT TRANSFORM THIS
            continue

        # Local entity is not foreign entity and local entity has foreign key(s)
        # Which are the same as the ID attributes of the foreign entity
        # Create a 1(foreign) to many(local) relationship 
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
    # end
    return

def createManyToManyRelationship(T, entities):
    """
    Given a relation object representing a "weak" relation type, transform the relation
    into a relationship between two existing entities, with the regular attributes of 
    the relation belonging to the relationship.
    
    Parameters
    ----------
    T: a relation object representing a "weak" type relation

    entities: array of existing entity objects

    Returns
    -------
    None

    """

    # Get all regular attributes belonging to the relation
    regularAttributes = [a.getName() for a in T.getAttributes() 
                         if (not a.isForeignKey()) and (a.isConcreteAttribute())]

    # Get names of all foreign key attributes belonging to the relation
    FKAttributeNames = [a.getName() for a in T.getAttributes() if a.isForeignKey()]
    
    relatedEntities = []

    # Find both entities referefnced by the foreign keys of the relation
    for E in entities:
        for A in E.getIDAttribs():
            add = True
            if(not A.getName() in FKAttributeNames):
                add = False
            if(add and not E.getName() in relatedEntities):
                relatedEntities.append(E)

    # Add a many (local) to many (foreign) relationship to the related entities
    # Include regular attributes as attributes of the relationship 
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
def EERToARM(entities):
    """
    Given a JSON representation of an ER conceptual model, transform and produce a JSON 
    representation of the schema as an ARM.

    Parameters
    ----------
    entities: a dictionary containing the ER model data 

    filePathWrite: the directory where the JSON file output must be written to

    Returns
    -------
    entities: an array of entity objects representing the resultanting from
              the transformation. 
    """

    entities = np.array(readEER(entities)) # read in array of entities from JSON file
    strongEntities = np.array([E for E in entities if E.isStrongEntity()]) 
    weakEntities = np.array([E for E in entities if not E.isStrongEntity()])
    relations = np.array([])

    # For each strong entity E, create a Relation TE, include all FK and PK (pathFD) constraints 
    T = StrongEntityToRelation(strongEntities)
    relations = np.concatenate([relations, T])

    # For each weak entity E create a relation TE, include all FK and PK (pathFD) constraints
    T = WeakEntityToRelation(weakEntities, strongEntities)
    relations = np.concatenate([relations, T])

    alreadyProcessed = [] # store foreign entity references which have already been processed

    # Consider all relationships between entities; transform accordingly
    for LE in strongEntities:
        for R in LE.getRelationships():
            # local and foreign entity tuple 
            pair = sorted((LE.getName(), R.getEntityName())) 

            # A one to one relationship between entities
            oneToOne = (R.getLocalRelationship() == RelationTypes.EXACTLY_ONE.value and 
                        R.getForeignRelationship() == RelationTypes.EXACTLY_ONE.value)

            # A one to one relationship between entities
            manyToOne = (R.getLocalRelationship() == RelationTypes.ZERO_OR_MANY.value and 
                        R.getForeignRelationship() == RelationTypes.EXACTLY_ONE.value)

            # A many to many relationship between entities
            manyToMany = (R.getLocalRelationship() == RelationTypes.ZERO_OR_MANY.value and 
                          R.getForeignRelationship() == RelationTypes.ZERO_OR_MANY.value)

            # For each 1:1 relationship between relation S and T, include as an FK in S, 
            # the PK of T as a constraint
            if(oneToOne and not pair in alreadyProcessed):
                foreignEntityIndex = [x.getName() for x in strongEntities].index(R.getEntityName()) 
                FE = strongEntities[foreignEntityIndex] 
                oneToOneTransform(LE, FE, R)
                alreadyProcessed.append(pair)
                
            # For each 1:N relationship between S and T respectively, include as an FK in T, 
            # the PK of S as a constraint
            elif(manyToOne):
                foreignEntityIndex = [x.getName() for x in strongEntities].index(R.getEntityName()) 
                FE = strongEntities[foreignEntityIndex] 
                manyToOneTransform(LE, FE, relations)

            # For each M:N relationship between S and T create a new relation R and include 
            # as FK attributes the primary keys of S and T, which will together form the 
            # composite primary key for R. Include other regular attributes belonging to the relationship
            elif(manyToMany and not pair in alreadyProcessed):
                foreignEntityIndex = [x.getName() for x in strongEntities].index(R.getEntityName()) 
                FE = strongEntities[foreignEntityIndex] 
                T = manyToManyTransform(LE, FE, R) 
                relations = np.concatenate([relations, T])
                alreadyProcessed.append(pair) 

    # Store pathFD references in pathFD map
    PFDMap, nameMap = createPathFDMap(relations)

    # Add all covering & disjointness constraints based on pathFD map
    addDisjointCoveringConstraints(PFDMap, nameMap, relations)

    # Write resultant relations to file
    return writeARM(list(relations))

def StrongEntityToRelation(strongEntities):
    """
    For each strong entity, create a new relation. 
    Add to it regular and PK attributes.

    Additionally, create a new relation for each multivalued attribute.


    Parameters
    ----------
    strongEntities: an array of entity objects

    Returns:
    toReturn: an array of relation objects
    """
    toReturn = [] 
    multivaluedAttributes = []

    for E in strongEntities:
        # Create a new relation corresponding with the strong entity
        T = Relation(
                     name=E.name,
                     inheritsFrom="none",
                     )

        # Add the "self" reference 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=DataTypes.OID.value, 
                       isPFD=False,
                       isFK=False
                       )

        # Add all regular and PK attributes
        for A in E.getAttributes():
            # If A is not a composite attribute 
            if(len(A.getComposedOf()) == 0):

                # if A is multivalued, append to array to handle below
                if(A.isMultiValuedAttribute()):
                    multivaluedAttributes.append(A)

                # If A is a regular or PK attribute
                else:
                    T.addAttribute(
                                   name=A.getName(), 
                                   isConcrete=True,
                                   dataType=DataTypes.ANY_TYPE.value, 
                                   isPFD=A.isIdentifierAttribute(), 
                                   isFK=False
                                   )
            else:
                print("lost info: composite attribute",A.getName(), "belonging to", E.getName())

        toReturn.append(T) # append relation to list to be returned

        # For each multivalued attribute create a new relation
        for multivaluedAttribute in multivaluedAttributes:
            T = multivaluedToRelation(multivaluedAttribute, E.getIDAttribs())
            toReturn.append(T)

    # return list of relations
    return np.array(toReturn) 

def WeakEntityToRelation(weakEntities, strongEntities):
    """
    For each weak entity, create a new relation. 
    Add to it regular, PK and FK attributes.


    Parameters
    ----------
    weakEntities: an array of entity objects

    strongEntities: an array of entity objects

    Returns:
    toReturn: an array of relation objects
    """
    toReturn = []
    for W in weakEntities:

        # Check whether the associated entity is in an inheritence hierachy
        inheritsFrom = "none"
        for r in W.getRelationships():
            if(r.getForeignRelationship() == RelationTypes.INHERITS_FROM.value):
                inheritsFrom = r.getEntityName()

        # Create a new relation for each weak entity
        T = Relation(
                    name=W.getName(),
                    inheritsFrom=inheritsFrom,
                    )

        # Add the "self" attribute 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=DataTypes.OID.value, 
                       isPFD=False, 
                       isFK=False
                       )

        # Add all simple attributes
        for A in W.getAttributes():
            # If A is non-composite
            if(len(A.getComposedOf()) == 0):
                # If a weak entity has a multivalued attribute, log error
                if(A.isMultiValuedAttribute()):
                    print("Can't handle weak entities with multivalued attributes") 
                # A is a regular or PK attribute
                else:
                    T.addAttribute(
                                   name=A.getName(), 
                                   isConcrete=True, 
                                   dataType=DataTypes.ANY_TYPE.value, 
                                   isPFD=A.isIdentifierAttribute(), 
                                   isFK=False
                                   )
            # Lost info: composite attributes
            else:
                print("lost info: composite attribute",A.getName(), "belonging to", W.getName())

        # For each relationship W has with a strong entity, add an FK attribute to the associated relation
        for R in W.getRelationships():

            # get owner entity
            index = [x.getName() for x in strongEntities].index(R.entityName)
            ownerEntity = strongEntities[index]

            # Add FK attribute to the relation associated with W
            for A in ownerEntity.getIDAttribs():
                T.addAttribute(
                       name=A.getName(), 
                       isConcrete=False, 
                       dataType=DataTypes.OID.value, 
                       isPFD=True, 
                       isFK=True
                       )

        # Add relation to list to be returned
        toReturn.append(T) 

    return np.array(toReturn)

def multivaluedToRelation(attribute, FKAttributes):
    """
    Given a multivalued attribute, create a new relation with PFD attributes 
    made up partially of the PK attributes of the owner relation.

    Parameters
    ----------
    attribute: multivalued attribute

    FKAttributes: ID attributes of the foreign entity, to be added as foreign key 
                  attributes to the kew relaion.

    Returns
    -------
    T: relation corresponding to the multivalued attribute
    """
    # create new relation 
    T = Relation(
                 name=attribute.getName(),
                 inheritsFrom="none", # TO BE UPDATED
                 )

    # Add the "self" attribute 
    T.addAttribute(
                   name="self", 
                   isConcrete=False, 
                   dataType=DataTypes.OID.value, 
                   isPFD=False,
                   isFK=False
                   )

    # Add unique ID attribute 
    T.addAttribute(
                   name=attribute.getName()+"ID", 
                   isConcrete=True, 
                   dataType=DataTypes.ANY_TYPE.value, 
                   isPFD=True,
                   isFK=False
                   )

    # Add all FK attributes from owner entity
    for FKAttrib in FKAttributes:
        T.addAttribute(
                   name=FKAttrib.getName(), 
                   isConcrete=False, 
                   dataType=DataTypes.OID.value, 
                   isPFD=True,
                   isFK=True
                   )

    # return relation
    return T

def oneToOneTransform(LE, FE, relations):
    """
    Given a local and foreign entity with a one-one relationship between them
    add as a foreign key to the associated foreign relation, the primary key
    of the associated local relation.

    Parameters
    ----------
    LE: local entity object

    FE: foreign entity object

    relations: array of relation objects

    Returns
    -------
    None
    """
    # get the index of the relation associated with the foreign entity
    foreignRelationIndex = [x.getName() for x in relations].index(FE.getName()) 
    FT = relations[foreignRelationIndex] # the relation corresponding to the foreign entity 

    # Add to the foreign relation as a foreign key, the ID attribute of the local entity
    for A in LE.getIDAttribs():
        FT.addAttribute(
                        name=A.getName(), 
                        isConcrete=False, 
                        dataType=DataTypes.OID.value, 
                        isPFD=False, 
                        isFK=True,
                        )
    return

def manyToOneTransform(LE, FE, relations):
    """
    Given a foreign and a local entity object with a many-one relationship between them,
    add to the associated local relation, as foreign key attributes, the ID attributes of
    the foreign entity.

    Parameters
    ----------
    LE: local entity object

    FE: foreign entity object

    relations: array of relation objects

    Returns
    -------
    None
    """
    # get associated local relation object
    localRelationIndex = [x.getName() for x in relations].index(LE.getName())
    T = relations[localRelationIndex]
    
    # Add as foreign keys to the local (many-side) relation the ID attributes of 
    # the foreign (one-side) entity   
    for A in FE.getIDAttribs():
        T.addAttribute(
               name=A.getName(), 
               isConcrete=False, 
               dataType=DataTypes.OID.value, 
               isPFD=False, 
               isFK=True
               )
    return

def manyToManyTransform(LE, FE, R):
    """
    Given a local and foreign entity with a many-many relationship between them
    create a new relation and add to it, as foreign key attributes, the primary
    key attributes of the associated relations. Also add any regular attributes 
    belonging to the relation.

    Parameters
    ----------
    LE: local entity object

    FE: foreign entity object

    Returns
    -------
    R: relationship object 
    """
    # Create a new relation corresponding to the Manay-Many relationship
    T = Relation(
                name="joinRelation["+LE.getName()+"-"+FE.getName()+"]",
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
    for A in LE.getIDAttribs(): 
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
    #return relation
    return np.array([T])

def createPathFDMap(relations):
    PFDMap = {}
    nameAdressMap = {}

    for relation in relations: 
        PFDMap[(relation.getName(), hex(id(relation)))] = sorted([a.getName()  for a in relation.getAttributes() if a.isPathFunctionalDependency()])

    return PFDMap, nameAdressMap

def addDisjointCoveringConstraints(PFDMap, nameMap, relations):
    for T in relations:
        pfdAttributes = sorted([A.getName() for A in T.getAttributes() if A.isPathFunctionalDependency()])
        for key in PFDMap.keys():
            if(PFDMap[key] == pfdAttributes):
                print(key)
                print(T.getName())
                print("######################")

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
