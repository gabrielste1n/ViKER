# ERMtoARM for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

import numpy as np
from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM
from Table import Relation, Entity
from Constants import DataTypes, RelationshipTypes
import json

def transform(entities):
    """
    Given a JSON representation of an ER conceptual model, transform and produce a JSON 
    representation of the schema as an ARM.

    Parameters
    ----------
    entities: an array of entity objects to be transformed

    Returns
    -------
    relations: an array of relaion objects representing the resultanting from
               the transformation. 

    log: a dictionary object with information regarding the transformation
    """

    log = {"Success":False, "couldNotTransform": []} # To save information about the transformation
    relations = np.array([]) # array of relation objects to be returned 

    # Check is the ER model is valid
    if (assertValidERModel(entities, log) == False):
        return relations, log # If not return failure

    # divide up strong and weak entities
    strongEntities = np.array([E for E in entities if E.isStrongEntity()]) 
    weakEntities = np.array([E for E in entities if not E.isStrongEntity()])

    # For each strong entity E, create a Relation TE, include all FK and PK (pathFD) constraints 
    T = StrongEntityToRelation(strongEntities, log)
    relations = np.concatenate([relations, T])

    # For each weak entity E create a relation TE, include all FK and PK (pathFD) constraints
    T = WeakEntityToRelation(weakEntities, strongEntities, log)
    relations = np.concatenate([relations, T])

    alreadyProcessed = [] # store foreign entity references which have already been processed

    # Consider all relationships between entities; transform accordingly
    for LE in strongEntities:
        for R in LE.getRelationships():
            # local and foreign entity tuple 
            pair = sorted((LE.getName(), R.getEntityName())) 

            # A one to one relationship between entities
            oneToOne = (R.getLocalRelationship() == RelationshipTypes.EXACTLY_ONE.value and 
                        R.getForeignRelationship() == RelationshipTypes.EXACTLY_ONE.value)

            # A one to one relationship between entities
            manyToOne = (R.getLocalRelationship() == RelationshipTypes.ZERO_OR_MANY.value and 
                        R.getForeignRelationship() == RelationshipTypes.EXACTLY_ONE.value)

            # A many to many relationship between entities
            manyToMany = (R.getLocalRelationship() == RelationshipTypes.ZERO_OR_MANY.value and 
                          R.getForeignRelationship() == RelationshipTypes.ZERO_OR_MANY.value)

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
    PFDMap = createPathFDMap(relations)

    # Add all disjointness constraints based on pathFD map
    addDisjointnessConstraints(PFDMap, relations)

    # Add all covering constraints based on ISA relationships
    addCoveringConstraints(relations)

    # Transformation succeeded
    log["Success"] = True

    # return relations and event log
    return relations, log

def StrongEntityToRelation(strongEntities, log):
    """
    For each strong entity, create a new relation. 
    Add to it regular and PK attributes.

    Additionally, create a new relation for each multivalued attribute.

    Parameters
    ----------
    strongEntities: an array of entity objects

    log: a dictionary object; an event log

    Returns
    -------
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
                       dataType=hex(id(T))+" ("+DataTypes.OID.value+")", 
                       isPFD=False,
                       isFK=False
                       )

        # Add all regular and PK attributes
        for A in E.getAttributes():
            # If A is not a composite attribute 
            if(len(A.getComposedOf()) == 0):

                # if A is multivalued, append to array to handle below
                if(A.isMultiValuedAttribute()):
                    log["couldNotTransform"].append(T.getName()+": lost multivalued property of attribute "+A.getName())
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
                log["couldNotTransform"].append(E.getName()+": lost composite attribute "+A.getName())

        toReturn.append(T) # append relation to list to be returned

        # For each multivalued attribute create a new relation
        for multivaluedAttribute in multivaluedAttributes:
            T = multivaluedToRelation(multivaluedAttribute, E.getIDAttribs())
            toReturn.append(T)

    # return list of relations
    return np.array(toReturn) 

def WeakEntityToRelation(weakEntities, strongEntities, log):
    """
    For each weak entity, create a new relation. 
    Add to it regular, PK and FK attributes.

    Parameters
    ----------
    weakEntities: an array of entity objects

    strongEntities: an array of entity objects

    log: a dictionary object; an event log

    Returns
    -------
    toReturn: an array of relation objects
    """
    toReturn = []
    for W in weakEntities:

        # Check whether the associated entity is in an inheritence hierachy
        inheritsFrom = "none"

        for r in W.getRelationships():
            if(r.getForeignRelationship() == RelationshipTypes.INHERITS_FROM.value):
                inheritsFrom = r.getEntityName()
                superEntityIndex = [E.getName() for E in strongEntities].index(r.getEntityName())
                superEntity = strongEntities[superEntityIndex]

        # Create a new relation for each weak entity
        T = Relation(
                    name=W.getName(),
                    inheritsFrom=inheritsFrom,
                    )

        memAddress = hex(id(T))
        isFK = False

        # If W inherits from a super entity, it's associated relation has "self" as 
        # a foreign key, referencing the relation associated with the super entity. 
        if(inheritsFrom != "none"):
            isFK = True
            memAddress = hex(id(superEntity))

        # Add the "self" attribute 
        T.addAttribute(
                       name="self", 
                       isConcrete=False, 
                       dataType=memAddress+" ("+DataTypes.OID.value+")", 
                       isPFD=False, 
                       isFK=isFK
                       )

        # Add all simple attributes
        for A in W.getAttributes():
            # If A is non-composite
            if(len(A.getComposedOf()) == 0):
                # If a weak entity has a multivalued attribute, log error
                if(A.isMultiValuedAttribute()):
                    log["couldNotTransform"].append(W.getName()+": cannot transform multivalued attribute "+A.getName()+" belonging to weak entity") 
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
                log["couldNotTransform"].append(W.getName()+": lost composite attribute "+A.getName())

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
                  attributes to the kew x.

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
                   dataType=hex(id(T))+" ("+DataTypes.OID.value+")", 
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
                   dataType=hex(id(T))+" ("+DataTypes.OID.value+")", 
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
    """
    Create a pathFD map such that pathfd(A1,...,An)-> self

    Parameters
    ----------
    relations: array of relation objects

    Returns
    -------
    PFDMap: pathfd dictionary
    """
    PFDMap = {}

    for relation in relations: 
        PFDMap[(relation.getName(), hex(id(relation)))] = sorted([a.getName()  for a in relation.getAttributes() if a.isPathFunctionalDependency()])

    return PFDMap

def addDisjointnessConstraints(PFDMap, relations):
    """
    Add disjointness constraints to each relation based on the memory
    location of the object represented by the relation (self)

    Parameters
    ----------
    PFDMap: maps pathfd(A1,...,An) -> self

    relations: array of relation objects

    Returns
    -------
    None
    """
    for T in relations:
        disjointWith = []
        coveredBy = []
        pfdAttributes = sorted([A.getName() for A in T.getAttributes() if A.isPathFunctionalDependency()])
        for key in PFDMap.keys():
            if(PFDMap[key] != pfdAttributes):
                disjointWith.append(key[0])

        T.setDisjointWith(disjointWith)

def addCoveringConstraints(relations):
    """
    Add covering constraints to the relation objects based on inheritence hierachies

    Parameters
    ----------
    relations: array of relation objects

    Returns
    -------
    None
    """
    for TSuper in relations:
        coveredBy = []
        for TSub in relations:
            if(TSuper.getName() == TSub.getInheritsFrom()):
                coveredBy.append(TSub.getName())
        TSuper.setCoveredBy(coveredBy)

def assertValidERModel(entities, log):
    """
    Determines whether or not there are elements in the ER model which will cause the transformation
    to fail.

    Parameters
    ----------
    entities: an array of entity objects 

    log: a dictionary object; an event log

    Returns
    -------
    canTransform: boolean value; False if the transformation is not possible, True otherwise
    """
    canTransform = True
    permissibleRelationshipTypes = [
                                    RelationshipTypes.EXACTLY_ONE.value, 
                                    RelationshipTypes.ZERO_OR_MANY.value, 
                                    RelationshipTypes.INHERITS_FROM.value
                                    ]
    for E in entities:
        for R in E.getRelationships():

            if(R.getLocalRelationship() not in permissibleRelationshipTypes):
                failError = E.getName()+": local relationship type "+R.getLocalRelationship()+" cannot be transformed"
                log["couldNotTransform"].append(failError)
                canTransform = False

            # Ensure there are no recursive ternary relationships between entities
            if(E.getName() == R.getEntityName()):
                failError = E.getName()+": Cannot transform unary, recursive relationship in ER model"
                log["couldNotTransform"].append(failError)
                canTransform = False
        
        # Ensure each strong entity has at least one identifier attribute
        if(E.isStrongEntity() and len(E.getIDAttribs()) == 0):
            failError = E.getName()+": Cannot transform strong entity with no identifier attribute."
            log["couldNotTransform"].append(failError)
            canTransform = False

    return canTransform

