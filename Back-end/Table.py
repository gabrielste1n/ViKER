# For ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

from Relationship import Relationship
from Attribute import ERAttribute, ARMAttribute

class Table:
    '''
    A Table is an abstract object which can be derived to be an ER Entity or ARM Relation
    '''

    def __new__(cls, *args, **kwargs):
        """
        Overidden __new__ method to prevent instatiation of abstract super class

        Parameters
        ----------
        cls: name of class being instantiated
        
        args: arguments

        kwargs: keyword arguments

        Returns
        -------
        None
        """

        if cls is Table:
            raise TypeError("base class Table may not be instantiated.")
        return object.__new__(cls)

    def __init__(self, name, attributes):
        """
        Instantiate a new Table object

        Parameters
        ----------
        self: object reference

        name: name of the Table object

        attributes: array attribute objects belonging to the table object

        Returns
        -------
        None
        """

        if(attributes is None):
            attributes = []
        self.name = name
        self.attributes = attributes

    def getName(self):
        """
        return name of Entity or Relation
        
        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.name: name of Table object
        """

        return self.name

    def getAttributes(self):
        """
        return attributes belonging to the Table object
        
        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.attributes: attributes belonging to Table object
        """

        return self.attributes

class Entity(Table):
    """An ER Entity is a Table"""

    def __init__(self, name, isStrong=False, attributes=None, relationships=None):
        """
        Instantiate a new Entity object
        
        Parameters
        ----------
        self: object reference

        name: name of Entity

        isStrong: boolean value; whether or not the entity is strong

        attributes: array of Attribute objects belonging to the Entity

        relationships: array of Relationship objects belonging to the Entity

        Returns
        -------
        None
        """
        Table.__init__(self, name, attributes)
        if(relationships is None):
            relationships = []
        self.isStrong = isStrong
        self.relationships = relationships

    def addRelationship(self, entityName, relationshipTypeLocal, relationshipTypeForeign, attributes=None):
        """
        Add a binary relationship with a given foreign Entity
        
        Parameters
        ----------
        self: object reference

        entityName: name of foreign Entity

        relationshipTypeLocal: the cardinality of the relationship on the local side

        relationshipTypeForeign: the cardinality of the relationship on the foreign side

        attributes: array of attribute names belonging to the Relationship

        Returns
        -------
        None
        """
        r = Relationship(entityName, relationshipTypeLocal, relationshipTypeForeign, attributes)
        self.relationships.append(r)

    def addAttribute(self, name, isIdentifier, isMultiValued=False, composedOf=None):
        """
        Create a new Attribute object and add it the attributes array belonging to the Entity

        Parameters
        ----------
        self: object reference

        name: name of the attribute

        isIdentifier: boolean; whether or not the attribute is an identifier of the Entity

        isMultivalued: boolean; whether or not the attrubute is multivalued

        composedOf: which attributes, if any, the attribute is composed of 

        Returns
        -------
        None
        """
        if(composedOf is None):
            composedOf = []
        A = ERAttribute(name, isIdentifier, isMultiValued, composedOf)
        self.attributes.append(A)

    def isStrongEntity(self):
        """
        Return boolean value indicating whether Entity is strong or weak

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.isStrong: boolean; whether or not the Entity is strong

        """
        return self.isStrong

    def getRelationships(self):
        """
        Return array of Relationship objects belonging to the Entity

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.relationships: array of Relationship objects
        """
        return self.relationships

    def getIDAttribs(self):
        """
        Return array of identifier attributes belonging to the Entity

        Parameters
        ----------
        self: object reference

        Returns
        -------
        a: array of Attributes objects such that each attribute is an identifier of the Enitty

        """
        a = [x for x in self.attributes if x.isIdentifier]
        return a

class Relation(Table):
    '''ARM Relation is a Table'''

    def __init__(self, name, attributes=None, inheritsFrom="none", coveredBy=None, disjointWith=None):
        """
        Instantiate a new Relation object

        Parameters
        ----------
        self: object reference

        name: the name of the relation object

        attributes: list; attribute objects belonging to the relation

        inheritsFrom: the super-relation from which the relation inherits

        coveredBy: list; the relations which cover the relation

        disjointWith: list; the relations with which the relation is disjoint

        Returns
        -------
        None
        """

        Table.__init__(self, name, attributes)

        if(coveredBy is None):
            coveredBy = []
        if(disjointWith is None):
            disjointWith = []
        
        self.inheritsFrom = inheritsFrom
        self.coveredBy = coveredBy
        self.disjointWith = disjointWith

    def addAttribute(self, name, isConcrete, dataType, isPFD, isFK):
        """
        append a new attribute object to the attribute array belonging to the Relation
        
        Parameters
        ----------
        self: object reference

        name: the name of the attribute

        isConcrete: boolean; whether or not the attribute is concrete (Integer, String etc.)

        dataType: the data type of the attribute (OID if not isConcrete)

        isPFD: is ths attribute A part of the attributes A1,..,An such that pathFD(A1,...,An) -> self

        isFK: boolean; whether or not the attribute a foreign key referencing another relation object

        Returns
        -------
        None
        """

        A = ARMAttribute(name, isConcrete, dataType, isPFD, isFK)
        self.attributes.append(A)

    def getInheritsFrom(self):
        """
        Return inheritsFrom instance variable

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.inheritsFrom

        """

        return self.inheritsFrom

    def getCoveredBy(self):
        """
        Return coveredBy instance variable (a list)
        
        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.coveredBy
        """

        return self.coveredBy

    def getDisjointWith(self):
        """
        Return disjointWith instance variable (a list)

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.disjointWith

        """

        return self.disjointWith

    def setDisjointWith(self, disjointWith):
        """
        Set disjointWith instance variable
        
        Parameters
        ----------
        self: object reference

        disjointWith: a list; names of relaion objects which are disjoint from the relation object

        Returns
        -------
        None
        """

        self.disjointWith = disjointWith

    def setCoveredBy(self, coveredBy):
        """
        Set coveredBy instance variable
        
        Parameters
        ----------
        self: object reference

        coveredBy: a list of relation objects which cover the realtion object

        Returns
        -------
        None
        """

        self.coveredBy = coveredBy

