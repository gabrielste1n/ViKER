from Relationship import Relationship
from Attribute import ERAttribute, ARMAttribute

class Table:
    '''A Table is an abstract object which can be derived to be an ER Entity or ARM Relation'''
    # Ensure that this base class cannot be instantiated by overriding the __new__ method belonging to Python's Object class.
    def __new__(cls, *args, **kwargs):
        if cls is Table:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls)

    def __init__(self, name, isStrong=False):
        # Create an entity
        self.name = name
        self.attributes = [] # List of attribute

class Entity(Table):
    '''ER Entity is a Table'''
    def __init__(self, name, isStrong=False):
        Table.__init__(self,name)
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
        
class Relation(Table):
    '''ARM Relation is a Table'''
    def __init__(self, name, inheritsFrom, coveredBy, disjointWith):
        Table.__init__(self,name)
        self.inheritsFrom = inheritsFrom
        self.coveredBy = coveredBy
        self.disjointWith = disjointWith

    def addAttribute(self, name, isConcrete, dataType, isPFD, isFK):
        self.attributes.append(ARMAttribute(name,
                                           isConcrete, 
                                           dataType, 
                                           isPFD, 
                                           isFK))