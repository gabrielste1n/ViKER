# constants file for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

from enum import Enum

class DataTypes(Enum):
    '''Specific types of data available'''
    ANY_TYPE = 'AnyType'
    INTEGER = 'Integer'
    FLOAT = 'FloatingPoint'
    STRING = 'String'
    OID = 'OID'

class RelationshipTypes(Enum):
    '''Types of relationships between entities'''
    EXACTLY_ONE = 'ExactlyOne'
    ZERO_OR_MANY = 'ZeroOrMany'
    INHERITS_FROM = 'ISA'

    