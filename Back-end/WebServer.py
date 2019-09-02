# Read in and write EER JSON objects for transformations
# Authors: St John Grimbly
# Date Created: 30 August 2019
# Version: Alpha v1.0

# Launch virtual environemnet in terminal using 'source venv/bin/activate'

import json
from Main import *
from flask import Flask, request, jsonify
from flask_cors import CORS

WebServer = Flask(__name__)
cors = CORS(WebServer)

def transform(json_file, fileType):
    print ("At transform method")
    if (fileType == "ARM"):
        # --------------------------------------------
        filename = '../Documentation/Phase 4/Test Cases/ERtoARM/ER/TestCase1_EER.JSON'
        with open(filename, 'r') as json_file: 
            entities = json.load(json_file)
        return entities
        # --------------------------------------------
        #return ARMToEER(json_file)
    print (json_file)
    return EERToARM(json_file)

def determine_model_type(json_file):
    # with open(file, 'r') as json_file:
    #         data = json.load(json_file)
    if 'entities' in json_file: 
        return 'EER'
    return 'ARM'

@WebServer.route('/')
def index():
    # TO DO: Display Markdown user guide for this application
    return ("WELCOME. THIS IS A SERVER ENDPOINT FOR CONVERTING BETWEEN " 
            "ARM AND EER MODELS.")

@WebServer.route('/api/transform', methods=['GET','POST'])
def transform_view():
    json_file = request.get_json(force=True)# JSON Dictionary
    
    #json_file = request.json
    if not json_file:
        return "No file"
    
    file_type = determine_model_type(json_file)

    transformed_file = transform(json_file, file_type)
    return transformed_file
    #return jsonify(transformed_file)
    

if __name__ == '__main__':
    WebServer.run(debug=True, host='0.0.0.0')