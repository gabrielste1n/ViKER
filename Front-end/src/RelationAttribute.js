// object to parse JSON into object
class RelationAttribute {
   
    constructor(attributeName, isConcrete, dataType, isPathFunctionalDependency, isFK){
        this.attributeName = attributeName;
        this.isConcrete = isConcrete;
        this.dataType = dataType;
        this.isPathFunctionalDependency = isPathFunctionalDependency;
        this.isFK = isFK;
    }
}

export default RelationAttribute;