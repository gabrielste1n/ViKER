class EntityModel {
   
    constructor(name, isStrong, attributes, relationships){
        this.name = name;
        this.isStrong = isStrong;
        this.attributes = attributes;
        this.relationships = relationships;
    }
}

export default EntityModel;