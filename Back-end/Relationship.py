
class Relationship:
    '''A Relationship details the cardinality between entities'''

    def __init__(self, entityName, relationshipTypeLocal, relationshipTypeForeign, attributes=None):
        """
        Constrictor for instantiating a new Relationship object

        Parameters
        ----------
        self: object reference

        entityName: name of the foreign entity

        relationshipTypeLocal: the cardinality of the relationship on the side of the local entity

        relationshipTypeForeign: the cardinality of the relationship on the side of the foreign entity

        attributes: list; names of attributes belonging to the relationship

        Returns
        -------
        None
        """

        if(attributes is None):
            attributes = []

        self.entityName = entityName
        self.relationshipTypeLocal = relationshipTypeLocal
        self.relationshipTypeForeign = relationshipTypeForeign
        self.attributes = attributes

    def getEntityName(self):
        '''
        Returns the instance variable entityName 

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.entityName
        '''

        return self.entityName

    def getLocalRelationship(self):
        '''
        Returns the instance variable relationshipTypeLocal 

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.relationshipTypeLocal
        '''

        return self.relationshipTypeLocal

    def getForeignRelationship(self):
        '''
        Returns the instance variable relationshipTypeForeign 

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.relationshipTypeForeign
        '''

        return self.relationshipTypeForeign

    def getAttributes(self):
        '''
        Returns the instance variable attributes 

        Parameters
        ----------
        self: object reference

        Returns
        -------
        self.attributes
        '''
        
        return self.attributes
        