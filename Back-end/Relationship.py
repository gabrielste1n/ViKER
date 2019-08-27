
class Relationship:
    '''A relationship represents the relation between entities'''
    def __init__(self, relationshipType, entityName):
        # Create a relationship
        self.relationshipType = relationshipType
        self.entityName = entityName