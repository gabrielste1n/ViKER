
class Relationship:
    '''A relationship represents the relation between entities'''
    def __init__(self, entityName, relationshipTypeLocal, relationshipTypeForeign, attributes):
        # Create a relationship
        self.entityName = entityName
        self.relationshipTypeLocal = relationshipTypeLocal
        self.relationshipTypeForeign = relationshipTypeForeign
        self.attributes = attributes