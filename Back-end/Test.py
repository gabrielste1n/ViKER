# Test Harness for ViKER Backend
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: September 2019
# Version: v1.0
# run using: python -m unittest Test

import unittest
from ReadWriteARM import *
from ReadWriteEER import *
from Main import EERToARM, ARMToEER
import json

path_read_JSONtest = '../Documentation/Phase 4/Test Cases/JSONReadWrite/Original/'
path_write_JSONtest = '../Documentation/Phase 4/Test Cases/JSONReadWrite/Generated/'

path_read_ERtoARM = '../Documentation/Phase 4/Test Cases/ERtoARM/ER/'
path_write_ERtoARM = '../Documentation/Phase 4/Test Cases/ERtoARM/Generated/'
path_target_ERtoARM = '../Documentation/Phase 4/Test Cases/ERtoARM/ARM/'

path_read_ARMtoER = '../Documentation/Phase 4/Test Cases/ARMtoER/ARM/'
path_write_ARMtoER = '../Documentation/Phase 4/Test Cases/ARMtoER/Generated/'
path_target_ARMtoER  = '../Documentation/Phase 4/Test Cases/ARMtoER/ER/'

class TestReadWriteJSON(unittest.TestCase):
    '''Unit tests for the ReadWriteARM class'''

    # Test using terminal with 
    # python -m unittest Test.TestReadWriteJSON

    def test_readWriteARM_case_1(self):
        test_tag = "Case1_ARM.JSON"
        relations = readARM(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeARM(relations), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ARM test case 1 passed.")

    def test_readWriteEER_case_1(self):
        test_tag = "Case1_EER.JSON"
        entities = readEER(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeEER(entities), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ER test case 1 passed.")

    def test_readWriteARM_case_2(self):
        test_tag = "Case2_ARM.JSON"
        relations = readARM(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeARM(relations), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ARM test case 2 passed.")

    def test_readWriteEER_case_2(self):
        test_tag = "Case2_EER.JSON"
        entities = readEER(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeEER(entities), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ER test case 2 passed.")

    def test_readWriteARM_case_3(self):
        test_tag = "Case3_ARM.JSON"
        relations = readARM(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeARM(relations), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ARM test case 3 passed.")

    def test_readWriteEER_case_3(self):
        test_tag = "Case3_EER.JSON"
        entities = readEER(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeEER(entities), path_write_JSONtest+test_tag)
        # assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ER test case 3 passed.")

    def test_readWriteARM_case_4(self):
        test_tag = "Case4_ARM.JSON"
        relations = readARM(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeARM(relations), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ARM test case 4 passed.")

    def test_readWriteEER_case_4(self):
        test_tag = "Case4_EER.JSON"
        entities = readEER(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeEER(entities), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ER test case 4 passed.")

    def test_readWriteARM_case_5(self):
        test_tag = "Case5_ARM.JSON"
        relations = readARM(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeARM(relations), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ARM test case 5 passed.")

    def test_readWriteEER_case_5(self):
        test_tag = "Case5_EER.JSON"
        entities = readEER(HelperMethods.readJSON(path_read_JSONtest+test_tag))
        HelperMethods.writeJSON(writeEER(entities), path_write_JSONtest+test_tag)
        assert(HelperMethods.filesEqual(path_read_JSONtest+test_tag, path_write_JSONtest+test_tag))
        print("JSON read/write ER test case 5 passed.")
    
class TestEERToARM(unittest.TestCase):
    """Unit tests for for Main.ERtoARM"""

    # Test using terminal with 
    # python -m unittest Test.TestEERToARM

    def test_EERToARM_case_1(self):
        test_case_ER = "TestCase1_EER.JSON"
        test_case_ARM = "TestCase1_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)

        if(log["Success"]): 
            print("Passed ER to ARM test case 1.")
        else:
            print("Failed ER to ARM test case 1.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_2(self):
        test_case_ER = "TestCase2_EER.JSON"
        test_case_ARM = "TestCase2_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)

        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 2.")
        else:
            print("\n\nFailed ER to ARM test case 2.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_3(self):
        test_case_ER = "TestCase3_EER.JSON"
        test_case_ARM = "TestCase3_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)

        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 3.")
        else:
            print("\n\nFailed ER to ARM test case 3.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_4(self):
        test_case_ER = "TestCase4_EER.JSON"
        test_case_ARM = "TestCase4_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)

        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 4.")
        else:
            print("\n\nFailed ER to ARM test case 4.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_5(self):
        test_case_ER = "TestCase5_EER.JSON"
        test_case_ARM = "TestCase5_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)

        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 5.")
        else:
            print("\n\nFailed ER to ARM test case 5.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_6(self): # include assert
        test_case_ER = "TestCase6_EER.JSON"
        test_case_ARM = "TestCase6_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)

        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 6.")
        else:
            print("\n\nFailed ER to ARM test case 6.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_7(self): # include assert
        test_case_ER = "TestCase7_EER.JSON"
        test_case_ARM = "TestCase7_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)
        
        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 7.")
        else:
            print("\n\nFailed ER to ARM test case 7.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_8(self): # include assert
        test_case_ER = "TestCase8_EER.JSON"
        test_case_ARM = "TestCase8_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)
        
        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 8.")
        else:
            print("\n\nFailed ER to ARM test case 8.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_8(self): # include assert
        test_case_ER = "TestCase8_EER.JSON"
        test_case_ARM = "TestCase8_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)
        
        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 8.")
        else:
            print("\n\nFailed ER to ARM test case 8.")

        HelperMethods.printLog(log)

    def test_EERToARM_case_9(self): # include assert
        test_case_ER = "TestCase9_EER.JSON"
        test_case_ARM = "TestCase9_ARM.JSON"

        entities = HelperMethods.readJSON(path_read_ERtoARM+test_case_ER)
        relations, log = EERToARM(entities)
        HelperMethods.writeJSON(relations, path_write_ERtoARM+test_case_ARM)
        
        if(log["Success"]): 
            print("\n\nPassed ER to ARM test case 9.")
        else:
            print("\n\nFailed ER to ARM test case 9.")

        HelperMethods.printLog(log)

class TestARMToEER(unittest.TestCase):
    """Unit tests for for Main.ARMtoER"""

    # Test using terminal with 
    # python -m unittest Test.TestARMToEER

    def test_ARMToEER_case_1(self):
        test_case_ER = "Case1_EER.JSON"
        test_case_ARM = "Case1_ARM.JSON"

        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)

        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 1.")
        else:
            print("\n\nFailed ARM to ER test case 1.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_2(self):
        test_case_ER = "Case2_EER.JSON"
        test_case_ARM = "Case2_ARM.JSON"

        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)

        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 2.")
        else:
            print("\n\nFailed ARM to ER test case 2.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_3(self):
        test_case_ER = "Case3_EER.JSON"
        test_case_ARM = "Case3_ARM.JSON"

        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)

        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 3.")
        else:
            print("\n\nFailed ARM to ER test case 3.")

        HelperMethods.printLog(log)

    def test_ARMToEERv_case_4(self):
        test_case_ER = "Case4_EER.JSON"
        test_case_ARM = "Case4_ARM.JSON"

        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)

        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 4.")
        else:
            print("\n\nFailed ARM to ER test case 4.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_5(self):
        test_case_ER = "Case5_EER.JSON"
        test_case_ARM = "Case5_ARM.JSON"

        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)

        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 5.")
        else:
            print("\n\nFailed ARM to ER test case 5.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_6(self):
        test_case_ER = "Case6_EER.JSON"
        test_case_ARM = "Case6_ARM.JSON"
        
        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)

        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 6.")
        else:
            print("\n\nFailed ARM to ER test case 6.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_7(self):
        test_case_ER = "Case7_EER.JSON"
        test_case_ARM = "Case7_ARM.JSON"
        
        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)
        
        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 7.")
        else:
            print("\n\nFailed ARM to ER test case 7.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_8(self):
        test_case_ER = "Case8_EER.JSON"
        test_case_ARM = "Case8_ARM.JSON"
        
        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)
        
        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 8.")
        else:
            print("\n\nFailed ARM to ER test case 8.")

        HelperMethods.printLog(log)

    def test_ARMToEER_case_9(self):
        test_case_ER = "Case9_EER.JSON"
        test_case_ARM = "Case9_ARM.JSON"
        
        relations = HelperMethods.readJSON(path_read_ARMtoER+test_case_ARM)
        entities, log = ARMToEER(relations)
        HelperMethods.writeJSON(entities, path_write_ARMtoER+test_case_ER)
        
        if(log["Success"]): 
            print("\n\nPassed ARM to ER test case 9.")
        else:
            print("\n\nFailed ARM to ER test case 9.")

        HelperMethods.printLog(log)

class HelperMethods():
    '''Helper methods needed for the functionality of unit tests in this file'''

    def filesEqual(f1_path, f2_path):
        with open(f1_path) as f1, open(f2_path) as f2:
            i = 0
            for l1, l2 in zip(f1,f2):
                if(l1 != l2):
                    print("Error in line "+str(i), l1, sep=": ")
                    return False
                i += 1
            return True

    def readJSON(filename):
        with open(filename, 'r') as f:
            datastore = json.load(f)
        return datastore

    def writeJSON(datastore, filename):
        with open(filename, 'w') as f:
            json.dump(datastore, f, indent=4, sort_keys=True)

    def printLog(log):
        for item in log["couldNotTransform"]:
            print(item)

if __name__ == '__main__':
    unittest.main()



