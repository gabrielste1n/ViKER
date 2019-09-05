
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

 1. Where the input model is rendered
 2. Where the output model is rendered
 3. Where the error log is printed
 4. Button to load model as a JSON file
 5. Button to send input model to server and transform to output model
 6. Saves the output model as a JSON file along with the error log

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

*Note: All diagrams can be moved around and interacted with!

# Examples
## EER
### ISA & Multivalued attribute
##### JSON

    {
    "entities": [
        {
            "attributes": [
                {
                    "AttributeName": "EmployeeID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "EmployeeName",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "EmployeeType",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "Skill",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": true
                }
            ],
            "isStrong": true,
            "name": "Employee",
            "relationships": [
                {
                    "Entity": "HourlyEmployee",
                    "RelationTypeForeign": "ISA",
                    "RelationTypeLocal": "ISA",
                    "relationAttributes": []
                },
                {
                    "Entity": "SalariedEmployee",
                    "RelationTypeForeign": "ISA",
                    "RelationTypeLocal": "ISA",
                    "relationAttributes": []
                },
                {
                    "Entity": "ContractEmployee",
                    "RelationTypeForeign": "ISA",
                    "RelationTypeLocal": "ISA",
                    "relationAttributes": []
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "HourlyRate",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": false,
            "name": "HourlyEmployee",
            "relationships": [
                {
                    "Entity": "Employee",
                    "RelationTypeForeign": "ISA",
                    "RelationTypeLocal": "ISA",
                    "relationAttributes": []
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "AnnualSalary",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": false,
            "name": "SalariedEmployee",
            "relationships": [
                {
                    "Entity": "Employee",
                    "RelationTypeForeign": "ISA",
                    "RelationTypeLocal": "ISA",
                    "relationAttributes": []
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "BillingRate",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": false,
            "name": "ContractEmployee",
            "relationships": [
                {
                    "Entity": "Employee",
                    "RelationTypeForeign": "ISA",
                    "RelationTypeLocal": "ISA",
                    "relationAttributes": []
                }
            ]
        }
      ]
    }

##### Model
![enter image description here](https://lh3.googleusercontent.com/iwZ5g93ibSvbLlbWSMsr8WEY0zlaoUnZkC9ktbbyu0xCH4BdK2Usg1Rnio9Vd5IHCVtbeDatUb8)

### Composite attributes
##### JSON

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
                    "composedOf": [
                        "CustomerState",
                        "CustomerCity",
                        "CustomerStreet"
                    ],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CustomerState",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CustomerCity",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CustomerStreet",
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

##### Model
![enter image description here](https://lh3.googleusercontent.com/L4M4KGo7iSQEF5_pEDsPIui-RNT3b4YhUT0Zkfe9hio7agwUsxmfe7NjYtaBPvT8JDGbFMzWUm8)

### Weak entity
##### JSON

    {
    "entities": [
        {
            "attributes": [
                {
                    "AttributeName": "DepartmentID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "DepartmentName",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": true,
            "name": "Department",
            "relationships": [
                {
                    "Entity": "Course",
                    "RelationTypeForeign": "ZeroOrMany",
                    "RelationTypeLocal": "ExactlyOne",
                    "relationAttributes": []
                },
                {
                    "Entity": "Professor",
                    "RelationTypeForeign": "ZeroOrMany",
                    "RelationTypeLocal": "ExactlyOne",
                    "relationAttributes": []
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "ProfessorID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "ProfessorName",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "OfficeNumber",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": true,
            "name": "Professor",
            "relationships": [
                {
                    "Entity": "Department",
                    "RelationTypeForeign": "ExactlyOne",
                    "RelationTypeLocal": "ZeroOrMany",
                    "relationAttributes": []
                },
                {
                    "Entity": "Class",
                    "RelationTypeForeign": "ZeroOrMany",
                    "RelationTypeLocal": "ExactlyOne",
                    "relationAttributes": []
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "CourseID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CourseName",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": true,
            "name": "Course",
            "relationships": [
                {
                    "Entity": "Department",
                    "RelationTypeForeign": "ExactlyOne",
                    "RelationTypeLocal": "ZeroOrMany",
                    "relationAttributes": []
                },
                {
                    "Entity": "Class",
                    "RelationTypeForeign": "ZeroOrMany",
                    "RelationTypeLocal": "ExactlyOne",
                    "relationAttributes": []
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "Selection",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "Term",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": false,
            "name": "Class",
            "relationships": [
                {
                    "Entity": "Course",
                    "RelationTypeForeign": "ExactlyOne",
                    "RelationTypeLocal": "ZeroOrMany",
                    "relationAttributes": []
                },
                {
                    "Entity": "Professor",
                    "RelationTypeForeign": "ExactlyOne",
                    "RelationTypeLocal": "ZeroOrMany",
                    "relationAttributes": []
                }
            ]
        }
      ]
    }

##### Model
![enter image description here](https://lh3.googleusercontent.com/HkJX5cgFj4JJoeD_iahDFQxXhdUmePHUMp3eYq713x1FAJYdIWmfo9ODAZ3pwt2iYXKhVVotUlM)

### Relationship attribute
##### JSON

    {
    "entities": [
        {
            "attributes": [
                {
                    "AttributeName": "EmployeeID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "EmployeeName",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "EmployeeBirthDate",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": true,
            "name": "Employee",
            "relationships": [
                {
                    "Entity": "Course",
                    "RelationTypeForeign": "ZeroOrMany",
                    "RelationTypeLocal": "ZeroOrMany",
                    "relationAttributes": [
                        "DateCompleted"
                    ]
                }
            ]
        },
        {
            "attributes": [
                {
                    "AttributeName": "CourseID",
                    "composedOf": [],
                    "isIdentifier": true,
                    "isMultiValued": false
                },
                {
                    "AttributeName": "CourseTitle",
                    "composedOf": [],
                    "isIdentifier": false,
                    "isMultiValued": false
                }
            ],
            "isStrong": true,
            "name": "Course",
            "relationships": [
                {
                    "Entity": "Employee",
                    "RelationTypeForeign": "ZeroOrMany",
                    "RelationTypeLocal": "ZeroOrMany",
                    "relationAttributes": [
                        "DateCompleted"
                    ]
                }
            ]
        }
     ]
    }

##### Model
![enter image description here](https://lh3.googleusercontent.com/_ga-KDkUm2VLVrD7X9aypOj4kj1hUntYRW-_L31x3UkJlMXzHxUb7JGDZwrUYPSjZu2DfIIQuUo)

## ARM
##### JSON

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
                    "AttributeName": "DepartmentID",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": true
                },
                {
                    "AttributeName": "DepartmentName",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                }
            ],
            "coveredBy": [],
            "disjointWith": ["Professor", "Course", "Class"],
            "inheritsFrom": "none",
            "name": "Department"
        },
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
                    "AttributeName": "DepartmentID",
                    "dataType": "OID",
                    "isConcrete": false,
                    "isFK": true,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "CourseID",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": true
                },
                {
                    "AttributeName": "CourseName",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                }
            ],
            "coveredBy": [],
            "disjointWith": ["Professor", "Department", "Class"],
            "inheritsFrom": "none",
            "name": "Course"
        },
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
                    "AttributeName": "DepartmentID",
                    "dataType": "OID",
                    "isConcrete": false,
                    "isFK": true,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "ProfessorID",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": true
                },
                {
                    "AttributeName": "ProfessorName",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "OfficeNumber",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                }
            ],
            "coveredBy": [],
            "disjointWith": ["Course", "Department", "Class"],
            "inheritsFrom": "none",
            "name": "Professor"
        },
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
                    "AttributeName": "CourseID",
                    "dataType": "OID",
                    "isConcrete": false,
                    "isFK": true,
                    "isPathFunctionalDependancy": true
                },
                {
                    "AttributeName": "ProfessorID",
                    "dataType": "OID",
                    "isConcrete": false,
                    "isFK": true,
                    "isPathFunctionalDependancy": true
                },
                {
                    "AttributeName": "Selection",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                },
                {
                    "AttributeName": "Term",
                    "dataType": "String",
                    "isConcrete": true,
                    "isFK": false,
                    "isPathFunctionalDependancy": false
                }
            ],
            "coveredBy": [],
            "disjointWith": ["Course", "Department", "Professor"],
            "inheritsFrom": "none",
            "name": "Class"
        }
      ]
    }

##### Model
![enter image description here](https://lh3.googleusercontent.com/kT9iRidglqZCnHyl5xiK_I9mISDvmwzIc3HZq1PdPr1zvhBYL1LRKreZDTsYo4fpkB4mOrXfPNA)
# Packages used
## Front-end

 - Node js
 - React js
 - Jointjs

## Back-end

 - Flask
 - virtualenv
 - numpy
 - Flask-CORS

