// object to parse json for entity attribute
class EntityAttribute {
   
    constructor(attributeName, isIdentifier, isMultiValued, composedOf){
        this.attributeName = attributeName;
        this.isIdentifier = isIdentifier;
        this.isMultiValued = isMultiValued;
        this.composedOf = composedOf;
    }
}

export default EntityAttribute;