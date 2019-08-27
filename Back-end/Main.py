# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from enum import Enum


'''Driver class for the ViKER Back-end implementation.'''
def EERToARM(filePath):
    # Produce a JSON representation of given schema in ARM
    entities = fetchEntities(filePath) # read in array of entities from JSON file
    strongEntities = [E for E in entities if E.isStrong]
    weakEntities = [E for E in entities if not E.isStrong]

    # For each strong entity E, create a Relation T 
    Relations = StrongEntityToRelation(strongEntities)

def ARMToEER(self):
    # Produce JSON representation of given schema in ER

def produceOOP(self, file):
    # Produce OOP representation of schema from given ARM or ER JSON file

def StrongEntityToRelation(E):
    # Create the relation
    T = Relation(
                name=E.name,
                inheritsFrom="none", # TO BE UPDATED
                coveredBy=[], 
                disjointWith=[]
                )

    # Add the "self" reference 
    T.addAttribute(
                   name="self", 
                   isConcrete=False, 
                   dataType=DataTypes.ANY_TYPE, 
                   isPFD=A.isIdentifier, 
                   isFK=False
                   )

    # Add all non-composite (simple) attributes
    for A in [x for x in E.attributes if len(x.composedOf) == 0]:
        T.addAttribute(
                       name=A.name, 
                       isConcrete=True, 
                       dataType=DataTypes.ANY_TYPE, 
                       isPFD=A.isIdentifier, 
                       isFK=False
                       )

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