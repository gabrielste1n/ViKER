class Attribute:
    '''An attribute is a characteristic of an entity'''
    # Ensure that this base class cannot be instantiated by overriding the __new__ method belonging to Python's Object class.
    def __new__(cls, *args, **kwargs):
        if cls is Attribute:
            raise TypeError("base class may not be instantiated")
        return object.__new__(cls)

    def __init__(self, name):
        # Create an attribute, specifying whether it is a foreign, primary 
        # (etc) key
        self.name = name

    def getName(self):
        """Returns attribute name"""
        return self.name
        
class ERAttribute(Attribute):
    '''An ER attribute is a characteristic of an ER entity'''
    def __init__(self, name, isIdentifier=False, isMultiValued=False, composedOf=[]):
        # Create an ER attribute
        Attribute.__init__(self, name)
        self.isIdentifier = isIdentifier
        self.isMultiValued = isMultiValued
        self.composedOf = composedOf

    def isIdentifierAttribute(self):
        """Returns true if it is an identifier"""
        return self.isIdentifier

    def isMultiValuedAttribute(self):
        """Returns true if it is multivalued"""
        return self.isMultiValued

    def getAttributeComposedOf(self):
        """Returns entity name"""
        return self.composedOf

class ARMAttribute(Attribute):
    '''An ARM attribute is a characteristics of an ARM relation'''
    def __init__(self, name, isConcrete, dataType, isPFD, isFK, FKPointer="none"):
        # Create an ARM attribute
        Attribute.__init__(self, name)
        self.isConcrete = isConcrete
        self.dataType = dataType
        self.isPFD = isPFD
        self.isFK = isFK
        self.FKPoint = FKPointer


    def isConcreteAttribute(self):
        """Returns true if it is concrete attribute"""
        return self.isConcrete

    def getDataType(self):
        '''Returns the data type of the attribute'''
        return self.dataType

    def isPathFunctionalDependency(self):
        '''Returns true if the attribute is a path functional dependencies'''
        return self.isPFD

    def isForeignKey(self):
        '''Returns true if the attribute is a foreign key'''
        return self.isFK