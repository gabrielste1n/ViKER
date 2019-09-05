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

def transform(json_file, file_type):
    """
    Given a json_file and the type of file (ARM/EER), contact the back-end classes and transform the file.
    Return the transformed file

    Parameters
    ----------
    json_file: The JSON ARM/EER file

    file_type: The type of the JSON file. i.e. ARM or EER
    Returns
    -------
    ARMToEER(json_file) or EERToARM(json_file): Transformed file
    """

    print ("At transform method")
    if (fileType == "ARM"):
        return ARMToEER(json_file)
    return EERToARM(json_file)

def determine_model_type(json_file):
    """
    Given a json_file, determine the type of the JSON file representation.

    Parameters
    ----------
    json_file: The JSON ARM/EER file

    Returns
    -------
    String 'EER' or 'ARM'
    """
    if 'entities' in json_file: 
        return 'EER'
    return 'ARM'

@WebServer.route('/')
def index():
    '''Index page for the server root directory.'''
    # TO DO: Display Markdown user guide for this application
    return ("WELCOME. THIS IS A SERVER ENDPOINT FOR CONVERTING BETWEEN " 
            "ARM AND EER MODELS.")

@WebServer.route('/api/transform', methods=['GET','POST'])
def transform_view():
    '''API endpoint for the transform method used in the JavaScript front-end.'''
    json_file = request.get_json(force=True)# JSON Dictionary
    
    #json_file = request.json
    if not json_file:
        return "No file"
    
    file_type = determine_model_type(json_file)
    transformed_file, log = transform(json_file, file_type)
    transformed_file['log'] = log

    return transformed_file    

if __name__ == '__main__':
    WebServer.run(debug=True, host='0.0.0.0')