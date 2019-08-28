from Relationship import Relationship
from Attribute import ERAttribute, ARMAttribute

class Table:
    '''A Table is an abstract object which can be derived to be an ER Entity or ARM Relation'''
    # Ensure that this base class cannot be instantiated by overriding the __new__ method belonging to Python's Object class.
    def __new__(cls, *args, **kwargs):
        if cls is Table:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls)

    def __init__(self, name):
        # Create an entity
        self.name = name
        self.attributes = [] # List of attribute
    
    def __init__(self, name, attributes):
        # Create an entity
        self.name = name
        self.attributes = attributes

    def getName(self):
        """Returns entity name"""
        return self.name

    def getAttributes(self):
        """Returns entity attributes"""
        return self.attributes

class Entity(Table):
    '''ER Entity is a Table'''

    # Instead of overloading constructor, 
    # we could just have one big constructor and give it default values.

    def __init__(self, name, isStrong=False):
        Table.__init__(self,name)
        self.isStrong = isStrong # True if strong entity, false if weak.
        self.relationships = [] # list of relationships belonging to this entity

    def __init__(self, name, isStrong=False, attributes=[], relationships=[]):
        Table.__init__(self,name,attributes)
        self.isStrong = isStrong # True if strong entity, false if weak.
        self.relationships = [] # list of relationships belonging to this entity

    def addRelationship(self, relationshipType, entityName):
        # Add relationship with given entity
        self.relationships.append(Relationship(relationshipType, entityName))

    def addAttribute(self, name, isIdentifier, isMultiValued, composedOf):
        self.attributes.append(ERAttribute(name, 
                                          isIdentifier, 
                                          isMultiValued,
                                          composedOf))

    def isStrongEntity(self):
        """Returns entity type"""
        return self.isStrong

    def getRelationships(self):
        """Returns entity relationships"""
        return self.relationships

    def getIDAttribs(self):
        a = [x for x in self.attributes if x.isIdentifier]
        return a
        
class Relation(Table):
    '''ARM Relation is a Table'''
    def __init__(self, name, inheritsFrom, coveredBy=[], disjointWith=[]):
        Table.__init__(self,name)
        self.inheritsFrom = inheritsFrom
        self.coveredBy = coveredBy
        self.disjointWith = disjointWith

    def addAttribute(self, name, isConcrete, dataType, isPFD, isFK, FKPointer = "none"):
        self.attributes.append(ARMAttribute(name,
                                           isConcrete, 
                                           dataType, 
                                           isPFD, 
                                           isFK,
                                           FKPointer))

    def getInheritsFrom(self):
        """Returns ARM ISA constraint"""
        return self.inheritsFrom

    def getCoveredBy(self):
        """Returns ARM covered-by constraint"""
        return self.coveredBy

    def getDisjointWith(self):
        """Returns ARM disjointness constraint"""
        return self.disjointWith
