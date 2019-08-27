# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 5 August 2019
# Version: Alpha v1.1

from enum import Enum

class Main:
    '''Driver class for the ViKER Back-end implementation.'''
    def convertToARM(self):
        # Produce a JSON representation of given schema in ARM
    
    def convertToER(self):
        # Produce JSON representation of given schema in ER

    def produceOOP(self, file):
        # Produce OOP representation of schema from given ARM or ER JSON file

class Table:
    '''A Table is an abstract object which can be derived to be an ER Entity or ARM Relation'''
    # Ensure that this base class cannot be instantiated by overriding the __new__ method belonging to Python's Object class.
    def __new__(cls, *args, **kwargs):
        if cls is Attribute:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls)

    def __init__(self, isStrong=False):
        # Create an entity
        self.attributes = [] # List of attribute
        self.relationships = [] # list of relationships belonging to this entity
        self.isStrong = isStrong # True if strong entity, false if weak.

        # TO DO: ADD INHERITANCE !! (AND OTHER CONSTRAINTS)

    def addRelationship(self, E):
        # Add relationship with given entity E

    def addAttribute(self, A):
        # Add attribute A to the this entity

class Entity(Table):
    '''ER Entity is a Table'''

class Relation(Table):
    '''ARM Relation is a Table'''

class DataTypes(Enum):
    '''Specific types of data available'''
    ANY_TYPE = 'AnyType'
    INTEGER = 'Integer'
    FLOAT = 'FloatingPoint'
    STRING = 'String'
    # OTHER/OBJECT ??

class Attribute:
    '''An attribute is a characteristic of an entity'''
    # Ensure that this base class cannot be instantiated by overriding the __new__ method belonging to Python's Object class.
    def __new__(cls, *args, **kwargs):
        if cls is Attribute:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls)

    def __init__(self, isPK=False, isFK=False):
        # Create an attribute, specifying whether it is a foreign, primary 
        # (etc) key
        self.isPK = isPK
        self.isFK = isFK
        
class ERAttribute(Attribute):
    '''An ER attribute is a characteristic of an ER entity'''
    def __init__(self, isPK=False, isFK=False, isMultiValued=False, composedOf=[]):
        # Create an ER attribute
        Attribute.__init__(self, isPK, isFK)
        self.isMultiValued = isMultiValued
        self.composedOf = composedOf

class ARMAttribute(Attribute):
    '''An ARM attribute is a characteristics of an ARM relation'''
    def __init__(self, isPK=False, isFK=False, isConcrete=True, dataType=DataTypes.ANY_TYPE):
        # Create an ARM attribute
        Attribute.__init__(self, isPK, isFK)
        self.dataType = dataType
        self.isConcrete = isConcrete

class RelationTypes(Enum):
    '''Types of relationships between entities'''
    ZERO_OR_MANY = 'ZeroOrMany'
    ZERO_OR_ONE = 'ZeroOrOne'
    EXACTLY_ONE = 'ExactlyOne'
    ONE_OR_MORE = 'OneOrMore'
    MANY = 'Many' 

class Relationship:
    '''A relationship represents the relation between entities'''
    def __init__(self, relationType, T1, T2):
        # Create a relationship
        self.relationType = relationType
        self.T1 = T1
        self.T2 = T2
