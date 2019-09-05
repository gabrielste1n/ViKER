# Driver class for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

from ReadWriteEER import readEER, writeEER
from ReadWriteARM import readARM, writeARM
import ARMtoER
import ERtoARM
import numpy as np


def ARMToEER(relations):
    """
    Stuff 
    """
    relations = np.array(readARM(relations))
    entities, log = ARMtoER.transform(relations)
    return writeEER(list(entities)), log

def EERToARM(entities):
    """
    Stuff
    """
    entities = np.array(readEER(entities)) # read in array of entities from JSON file
    relations, log = ERtoARM.transform(entities)
    return writeARM(list(relations)), log

