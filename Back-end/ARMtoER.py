# ARMtoER file for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import numpy as np
from Constants import DataTypes, RelationTypes
from Table import Relation, Entity
import json

def transform(relations):
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
              the transformation

    log: a dictionary object with information regarding the transformation
    """

    entities = [] # array for output entity objects

    # Sorting arrays for different catagories of relation objects
    weakRelationTypes = []
    StrongOrRegularRelationTypes = []

    log = {"Success":False, "couldNotTransform": []} # To save information about the transformation

    # loop through all relation objects
    for T in relations:

        # A relation type can be strong, regular or weak (see function)
        relationType = getRelationshipType(T)

        if(relationType=="strong"):
            # If relationType is "strong" create a strong entity 
            entities.append(createEntity(T, log, isStrong=True))
            StrongOrRegularRelationTypes.append(T)
 
        elif(relationType == "regular"):
            # If relationType is "regular" create a weak entity 
            entities.append(createEntity(T, log, isStrong=False))
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
    
    # Append lost information about covering and disjointness constraints to log
    appendLostConstraintInfo(relations, log)

    # Transformation succeeded
    log["Success"] = True

    # Write resultant entities to file
    return entities, log

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

def createEntity(T, log, isStrong):
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
            log["couldNotTransform"].append(T.getName()+": lost data type "+ARMattrib.getDataType()+" for attribute "+ARMattrib.getName())
        else:
            if(ARMattrib.getName() == "self"):
                log["couldNotTransform"].append(T.getName()+": lost PK reference to self -> "+hex(id(T)))
            else:
                log["couldNotTransform"].append(T.getName()+": lost FK reference "+ARMattrib.getName())
    
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

def appendLostConstraintInfo(relations, log):
    for T in relations:
        for cb in T.getCoveredBy():
            log["couldNotTransform"].append(T.getName()+": lost covering constraint info; covered by "+str(cb))
        for dw in T.getDisjointWith():
            log["couldNotTransform"].append(T.getName()+": lost disjointness constraint info; disjoint with "+str(dw))

