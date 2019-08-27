# Read in and write ARM JSON objects for transformations
# Authors: St John Grimbly & Jeremy du Plessis
# Date Created: 27 August 2019
# Version: Beta v1.0

import json

def read(filename):
    with open(filename, 'r', encoding='utf8', errors='ignore') as json_file:
        relations = json.load(json_file)
        for relation in relations['relations']:
            

