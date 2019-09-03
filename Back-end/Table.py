from Relationship import Relationship
from Attribute import ERAttribute, ARMAttribute

class Table:
    '''A Table is an abstract object which can be derived to be an ER Entity or ARM Relation'''
    def __new__(cls, *args, **kwargs):
        if cls is Table:
            raise TypeError("base class Table may not be instantiated.")
        return object.__new__(cls)

    def __init__(self, name, attributes):
        """Instantiate a new Table object"""
        if(attributes is None):
            attributes = []
        self.name = name
        self.attributes = attributes

    def getName(self):
        """return name of Entity or Relation"""
        return self.name

    def getAttributes(self):
        """return attributes belonging to Entity or Relation"""
        return self.attributes


class Entity(Table):
    def __init__(self, name, isStrong=False, attributes=None, relationships=None):
        """Instantiate a new Entity object"""
        Table.__init__(self, name, attributes)
        if(relationships is None):
            relationships = []
        self.isStrong = isStrong
        self.relationships = relationships

    def addRelationship(self, entityName, relationshipTypeLocal, relationshipTypeForeign, attributes=None):
        """Add a binary relationship with a given entity"""
        r = Relationship(entityName, relationshipTypeLocal, relationshipTypeForeign, attributes)
        self.relationships.append(r)

    def addAttribute(self, name, isIdentifier, isMultiValued=False, composedOf=None):
        """Add a new attribute to the Entity"""
        if(composedOf is None):
            composedOf = []
        A = ERAttribute(name, isIdentifier, isMultiValued, composedOf)
        self.attributes.append(A)

    def isStrongEntity(self):
        """Return boolean value indicating whether Entity is strong or weak"""
        return self.isStrong

    def getRelationships(self):
        """return array of relationship objects"""
        return self.relationships

    def getIDAttribs(self):
        """return array of identifier attributes"""
        a = [x for x in self.attributes if x.isIdentifier]
        return a

class Relation(Table):
    '''ARM Relation is a Table'''
    def __init__(self, name, attributes=None, inheritsFrom="none", coveredBy=None, disjointWith=None):
        """Instantiate a new Relation object"""
        Table.__init__(self, name, attributes)
        if(coveredBy is None):
            coveredBy = []
        if(disjointWith is None):
            disjointWith = []
        self.inheritsFrom = inheritsFrom
        self.coveredBy = coveredBy
        self.disjointWith = disjointWith

    def addAttribute(self, name, isConcrete, dataType, isPFD, isFK, FKPointer = "none"):
        """Add a new attribute to the Relation"""
        A = ARMAttribute(name, isConcrete, dataType, isPFD, isFK, FKPointer)
        self.attributes.append(A)

    def getInheritsFrom(self):
        """Return inheritsFrom (String)"""
        return self.inheritsFrom

    def getCoveredBy(self):
        """return coveredBy (list)"""
        return self.coveredBy

    def getDisjointWith(self):
        """return disjointWith (list)"""
        return self.disjointWith