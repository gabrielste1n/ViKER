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
        
class ERAttribute(Attribute):
    '''An ER attribute is a characteristic of an ER entity'''
    def __init__(self, name, isIdentifier=False, isMultiValued=False, composedOf=[]):
        # Create an ER attribute
        Attribute.__init__(self, name)
        self.isIdentifier = isIdentifier
        self.isMultiValued = isMultiValued
        self.composedOf = composedOf

class ARMAttribute(Attribute):
    '''An ARM attribute is a characteristics of an ARM relation'''
    def __init__(self, name, isConcrete, dataType, isPFD, isFK):
        # Create an ARM attribute
        Attribute.__init__(self, name)
        self.isConcrete = isConcrete
        self.dataType = dataType
        self.isPFD = isPFD
        self.isFK = isFK