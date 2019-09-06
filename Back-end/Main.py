# Driver for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0

from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM
import ARMtoEER
import EERtoARM
import numpy as np


def ARMToEER(relations):
    """
    Driver method for the ARM to ER transformation function ARMtoER.transform()

    Parameters
    ----------
    relations: array of relation objects

    Returns
    -------
    JSONEntities: transformed entity objects in JSON format

    log: an event log of the transformation
    """
    
    relations = np.array(readARM(relations))
    entities, log = ARMtoEER.transform(relations)
    JSONEntities = writeEER(list(entities))
    return JSONEntities, log

def EERToARM(entities):
    """
    Driver method for the ER to ARM transformation function ERtoARM.transform()

    Parameters
    ----------
    relations: array of relation objects

    Returns
    -------
    JSONRelations: transformed relation objects in JSON format

    log: an event log of the transformation
    """

    entities = np.array(readEER(entities)) # read in array of entities from JSON file
    relations, log = EERtoARM.transform(entities)
    JSONRelations = writeARM(list(relations))
    return JSONRelations, log

