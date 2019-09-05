// object to pardse JSON into object
class RelationModel {
   
    constructor(name, attributes, inheritsFrom, coveredBy, disjointWith){
        this.name = name;
        this.attributes = attributes;
        this.inheritsFrom = inheritsFrom;
        this.coveredBy = coveredBy;
        this.disjointWith = disjointWith;
    }
}

export default RelationModel;