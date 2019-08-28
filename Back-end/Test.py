import unittest
from ReadWriteARM import *
from ReadWriteEER import *
from Main import EERToARM

path_read = '../Documentation/Phase 4/Test Cases/'
path_write = '../Documentation/Phase 4/Generated/'

class HelperMethods():
    '''Helper methods needed for the functionality of unit tests in this file'''

class TestReadWriteJSON(unittest.TestCase):
    '''Unit tests for the ReadWriteARM class'''

    # Test using terminal with 
    # python -m unittest Test.TestReadWriteJSON

    def test_readWriteARM_case_1(self):
        relations = readARM(path_read+"Case1_ARM.JSON")
        writeARM(path_write+'TestCase1_ARM.JSON', relations)
        #assert()

    def test_readWriteEER_case_1(self):
        entities = readEER(path_read+"Case1_EER.JSON")
        writeEER(path_write+'TestCase1_EER.JSON', entities)

    def test_readWriteARM_case_2(self):
        relations = readARM(path_read+"Case2_ARM.JSON")
        writeARM(path_write+'TestCase2_ARM.JSON', relations)

    def test_readWriteEER_case_2(self):
        entities = readEER(path_read+"Case2_EER.JSON")
        writeEER(path_write+'TestCase2_EER.JSON', entities)

    def test_readWriteARM_case_3(self):
        relations = readARM(path_read+"Case3_ARM.JSON")
        writeARM(path_write+'TestCase3_ARM.JSON', relations)

    def test_readWriteEER_case_3(self):
        entities = readEER(path_read+"Case3_EER.JSON")
        writeEER(path_write+'TestCase3_EER.JSON', entities)

    def test_readWriteARM_case_4(self):
        relations = readARM(path_read+"Case4_ARM.JSON")
        writeARM(path_write+'TestCase4_ARM.JSON', relations)

    def test_readWriteEER_case_4(self):
        entities = readEER(path_read+"Case4_EER.JSON")
        writeEER(path_write+'TestCase4_EER.JSON', entities)

    def test_readWriteARM_case_5(self):
        relations = readARM(path_read+"Case5_ARM.JSON")
        writeARM(path_write+'TestCase5_ARM.JSON', relations)

    def test_readWriteEER_case_5(self):
        entities = readEER(path_read+"Case5_EER.JSON")
        writeEER(path_write+'TestCase5_EER.JSON', entities)
    
# class TestEERToARM(unittest.TestCase):

#     def test_EERToARM_case_1(self):
#         EERToARM(path_write+"TestCase1_EER.JSON")
#         #assert()


if __name__ == '__main__':
    unittest.main()