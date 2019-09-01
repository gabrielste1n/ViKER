# Read in and write EER JSON objects for transformations
# Authors: St John Grimbly
# Date Created: 30 August 2019
# Version: Alpha v1.0

from Main import *
from flask import Flask, request, jsonify

WebServer = Flask(__name__)

def transform(json_file, fileType):
    if (fileType == "ARM"):
        return ARMToEER(json_file)
    return EERToARM(json_file)

@WebServer.route('/')
def index():
    # TO DO: Display Markdown user guide for this application
    return ("WELCOME. THIS IS A SERVER ENDPOINT FOR CONVERTING BETWEEN" 
            "ARM AND EER MODELS.")

@WebServer.route('/convert-file', methods=['GET','POST'])
def transform_view():
    json_file = request.get_json()
    if not json_file:
        return "No file"

    transformed_file = transform(json_file)
    return jsonify(transformed_file)

if __name__ == '__main__':
    WebServer.run(debug=True, host='0.0.0.0')