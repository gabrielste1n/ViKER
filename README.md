# ViKER User Manual

# How to start the python server (back-end)

Using the terminal:

    $ cd Back-end/
    $ source venv/bin/activate
    $ python WebServer.py

# How to start the node server (front-end)

Using the terminal:

    $ cd Front-end/
    $ npm install
    $ npm start
Your browser will then open on [http://localhost:3000/](http://localhost:3000/)

# User Interface

  ![enter image description here](https://lh3.googleusercontent.com/Wkl2bOji6vcVqEFlGRmFsz9Eehf626xd6FSC0WQgiMWOWFozfyYMpQ__zrvkmHvUU4qqx1FeG6A)

1.) Where the input model is rendered
2.) Where the output model is rendered
3.) Where the error log is printed
4.) Button to load model as a JSON file
5.) Button to send input model to server and transform to output model
6.) Saves the output model as a JSON file along with the error log

# What the models look like in JSON

## ARM representation

    {
    "relations": [
        {
            "attributes": [
                {
                    "AttributeName": "self",
                    "dataType": "OID",
                    "isConcrete": false,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "CustomerID",
                    "dataType": "Integer",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": true
                },
                {
                    "AttributeName": "CustomerName",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "CustomerAddress",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "CustomerPostalCode",
                    "dataType": "Integer",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                }
            ],
            "coveredBy": [],
            "disjointWith": [],
            "inheritsFrom": "none",
            "name": "Customer"
        }
	  ]
    }


## EER representation

    {
    "entities": [
        {
            "attributes": [
                {
                    "AttributeName": "CustomerID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CustomerName",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CustomerAddress",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CustomerPostalCode",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": true,
            "name": "Customer",
            "relationships": []
        }
      ]
    }

## Loading a model

1.) Click the 'Load Model' button
2.) The file chooser will open such as below:

![enter image description here](https://lh3.googleusercontent.com/M5aWE_6w4itrxtaKA_879yD-JIV1NyVQLBZt2Jp7W5zdt3HHRZeln15WR4TRajqCQPhcUhsGHfI)

3.) The model will then render such as below:

![enter image description here](https://lh3.googleusercontent.com/dB6nt4DjNLSIWYt6Fp5In7uHbj9cd0TStZfK7_ugI05at0FSYq091B7mwM4MBGrm-n7XGcf_Wa0)

4.) Click the 'Transform Model' button to transform the model and render the output model, such as below:

![enter image description here](https://lh3.googleusercontent.com/ln9TrNyBRgsOJza-5yg2YVBaveTWZqPC5AmDOZ0DuqYPY3JWFxfDPnhDgtL8MeYz1ReXTN6rOMQ)

5.) You can then save the output model and the error report as JSON, by clicking the 'Save Transformation Report' button. You will see the file being downloaded, such as below:

![enter image description here](https://lh3.googleusercontent.com/5qhItzjXL5VkhpHfkzwfWV1Eg-eOn5cOiGoVaPX5TzzxvZKysIxJ5ZllH1tNzl3fou0Ue97hnZA)

6.) You can also transform from ARM to EER, the same way!

![enter image description here](https://lh3.googleusercontent.com/TCmIfI6iG9C3pq9dMTaVuW_w-Na1okAKMUbeer1yhuY15ZxrnBXo6PCARsLoWtJCyTmQSwe-7vo)

# Packages used
## Front-end

 - Node js
 - React js
 - Jointjs
- heroku
## Back-end

 - Flask
 - virtualenv
 - numpy
 - Flask-CORS
 - heroku
