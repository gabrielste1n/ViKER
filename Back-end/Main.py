# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 5 August 2019
# Version: 1.0

from enunm import Enum

class Main:
    '''Driver class for the ViKER Back-end implementation.'''
    def convertToARM(self):
        # Produce a JSON representation of given schema in ARM
    
    def convertToER(self):
        # Produce JSON representation of given schema in ER

    def produceOOP(self, file):
        # Produce OOP representation of schema from given ARM or ER JSON file


class Entitiy:
    '''An Entity is an abstract object '''
    def __init__(self, isStrong=False):
        # Create an entity
        self.attributes = [] # List of attribute
        self.isStrong = isStrong # True if strong entity, false if weak.

    def addRelationship(self, E):
        # Add relationship with given entity E

    def addAttribute(self, A):
        # Add attribute A to the this entity


class Attribute:
    '''An attribute is a characteristic of an entity'''
    def __init__(self, isPK=False, isFK=False, isMultiValued=False,
         dataType='AnyType', composedOf=[]):
        # Create an attribute, specifying whether it is a foreign, primary 
        # (etc) key
        self.isPK = isPK
        self.isFK = isFK
        self.isMultiValued = isMultiValued
        self.dataType = dataType
        self.composedOf = composedOf

class RelationTypes(Enum):
    '''Types of relationships between entities'''
    ZERO_OR_MANY = 'ZeroOrMany'
    ZERO_OR_ONE = 'ZeroOrOne'
    EXACTLY_ONE = 'ExactlyOne'
    ONE_OR_MORE = 'OneOrMore'
    MANY = 'Many' 

class Relationship:
    '''A relationship represents the relation between entities'''
    def __init__(self, relationType, T1, PK, T2, FK):
        # Create a relationship
        self.relationType = relationType
        self.T1 = T1
        self.PK = PK
        self.T2 = T2
        self.FK = FK
