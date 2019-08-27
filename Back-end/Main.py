# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from enum import Enum

class Main:
    '''Driver class for the ViKER Back-end implementation.'''
    def convertToARM(self):
        # Produce a JSON representation of given schema in ARM
    
    def convertToER(self):
        # Produce JSON representation of given schema in ER

    def produceOOP(self, file):
        # Produce OOP representation of schema from given ARM or ER JSON file

class DataTypes(Enum):
    '''Specific types of data available'''
    ANY_TYPE = 'AnyType'
    INTEGER = 'Integer'
    FLOAT = 'FloatingPoint'
    STRING = 'String'
    OID = 'OID'

class RelationTypes(Enum):
    '''Types of relationships between entities'''
    ZERO_OR_MANY = 'ZeroOrMany'
    ZERO_OR_ONE = 'ZeroOrOne'
    EXACTLY_ONE = 'ExactlyOne'
    ONE_OR_MORE = 'OneOrMore'
    MANY = 'Many' 