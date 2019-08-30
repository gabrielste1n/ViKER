
class Relationship:
    '''A relationship represents the relation between entities'''
    def __init__(self, entityName, relationshipTypeLocal, relationshipTypeForeign, attributes=None):
        # Create a relationship
        if(attributes is None):
            attributes = []
        self.entityName = entityName
        self.relationshipTypeLocal = relationshipTypeLocal
        self.relationshipTypeForeign = relationshipTypeForeign
        self.attributes = attributes

    def getEntityName(self):
        '''Returns the name of the entity it is related to'''
        return self.entityName

    def getLocalRelationship(self):
        '''Returns the local relationship'''
        return self.relationshipTypeLocal

    def getForeignRelationship(self):
        '''Returns the local relationship'''
        return self.relationshipTypeForeign

    def getAttributes(self):
        '''Returns the relationship attributes'''
        return self.attributes
        