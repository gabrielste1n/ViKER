class RelationModel {
   
    constructor(name, attributes, inheritsFrom, coveredBy, disjointWith){
        this.name = name;
        this.attributes = attributes;
        this.inheritsFrom = inheritsFrom;
        this.coveredBy = coveredBy;
        this.disjointWith = disjointWith;
    }
}