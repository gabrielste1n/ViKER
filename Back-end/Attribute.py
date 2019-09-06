# For ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

class Attribute:
    '''An attribute is a characteristic of an entity'''

    def __new__(cls, *args, **kwargs):
        """
        Overidden __new__ method to prevent instatiation of abstract super class

        Parameters
        ----------
        cls: name of class being instantiated
        
        args: arguments

        kwargs: keyword arguments

        Returns
        -------
        None
        """

        if cls is Attribute:
            raise TypeError("base class may not be instantiated")

        return object.__new__(cls)

    def __init__(self, name):
        """
        Instantiate a new Attribute object

        Parameters
        ----------
        self: object reference

        name: name of the Attribute

        Returns
        -------
        None
        """

        self.name = name

    def getName(self):
        """
        Returns attribute name
        
        Parameters
        ----------
        self: object reference

        Returns
        -------
        None
        """

        return self.name
        
class ERAttribute(Attribute):
    '''An ER attribute is a characteristic of an ER entity'''

    def __init__(self, name, isIdentifier=False, isMultiValued=False, composedOf=None):
        """
        Constrictor for instatiating a new ERAttribute object (an attribute belonging to an Entity object)

        Parameters
        ----------
        self: object reference

        name: name of the ERAttribute

        isIdentifier: boolean; whether or not the attribute is an identifier of the entity

        isMultivalued: boolean; whether or not the attribute is multivalued

        composedOf: list; names of the attributes of which the attribute is composed

        Returns
        -------
        None 
        """

        Attribute.__init__(self, name)

        if(composedOf is None):
            composedOf = []

        self.isIdentifier = isIdentifier
        self.isMultiValued = isMultiValued
        self.composedOf = composedOf

    def isIdentifierAttribute(self):
        """
        returns instance variable isIdentifier

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.isIdentifier
        """

        return self.isIdentifier

    def isMultiValuedAttribute(self):
        """
        Returns instance variable isMultivalued
        
        Parameters
        ----------
        self: object reference

        Returns
        -------
        None
        """

        return self.isMultiValued

    def getAttributeComposedOf(self):
        """
        Returns instance variable composedOf

        Parameters
        ----------
        self: object reference
        
        Returns
        -------
        self.composedOf
        """

        return self.composedOf

    def getComposedOf(self):
        """
        returns composedOf instance variable

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.composedOf
        """

        return self.composedOf

class ARMAttribute(Attribute):
    '''An ARM attribute is a characteristic of an ARM relation'''

    def __init__(self, name, isConcrete, dataType, isPFD=False, isFK=False):
        """
        Constrictor for instatiating a new ARMAttribute object (an attribute belonging to an Relation object)

        Parameters
        ----------
        self: object reference

        name: name of the ARMAttribute

        isConcrete: boolean; whether or not the attribute is concrete (Integer, String etc.)

        dataType: the data type of the attribute (OID if not isConcrete)

        isPFD: is ths attribute A part of the attributes A1,..,An such that pathFD(A1,...,An) -> self

        isFK: boolean; whether or not the attribute a foreign key referencing another relation object

        Returns
        -------
        None 
        """

        Attribute.__init__(self, name)
        self.isConcrete = isConcrete
        self.dataType = dataType
        self.isPFD = isPFD
        self.isFK = isFK

    def isConcreteAttribute(self):
        """
        Returns isConcrete instance variable

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.isConcrete
        """
        
        return self.isConcrete

    def getDataType(self):
        '''
        Returns the data type of the attribute
        
        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.dataType
        '''

        return self.dataType

    def isPathFunctionalDependency(self):
        '''
        Returns the instance varible isPFD

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.isPFD
        '''

        return self.isPFD

    def isForeignKey(self):
        '''
        Returns the instance variable isFK 

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.isFK
        '''

        return self.isFK



        