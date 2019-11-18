# DataRobot ODSC Europe 2019 Hands-on Training

This is for DataRobot ODSC Europe 2019 Hands-on Training.

This contains `Dockerfile` to make it easy to get up and running with
Hands-on Training via [Docker](http://www.docker.com/).


## 1. Installing Docker
General installation instructions are
[on the Docker site](https://docs.docker.com/installation/), but we give some
quick links here:

* [OSX](https://www.docker.com/docker-mac)
* [Windows](https://www.docker.com/docker-windows)
* [Ubuntu](https://www.docker.com/docker-ubuntu)

## 2. Running the container

### 2.1 run a new Docker container
Linux/MacOS/Windows:

    $ docker build -t dr-odsc-jupyter-python3 dr-odsc-jupyter-python3/.
    $ docker run -p 8890:8890 -p 8080:8080 -v -it --rm dr-odsc-jupyter-python3


>This container setup:
>- Python 3.7
>- DataRobot
>- flask
>- scikit-learn 
>- sklearn
>- jupyter
>- scipy
>- numpy
>- pandas
>- wtforms
>- seaborn

### 2.2 start flask app for prediction API endpoint

	$ docker ps -a
	$ docker exec -it 'container_id' bash
	$ cd /DataRobot_ODSC/Flask_App/python_model/
	$ ./start_server.sh


### 2.3 folder structure

```

├── DataRobot_ODSC				
│   ├── DR_Python_API				# DataRobot Python client
│   │   ├── API_Basics.ipynb
│   │   ├── API_model_factory.ipynb
│   │   └── media
│   │       ├── DataRobot.png
│   │       ├── credentials_1.png
│   │       ├── credentials_2.png
│   │       ├── credentials_3.png
│   │       ├── model_id.png
│   │       ├── prediction_api.png
│   │       └── ts_mind_blown.jpg
│   ├── Data                        # Data we will use during the training
│   │   ├── 10k_diabetes_ODSC_Prediction.csv
│   │   ├── 10k_diabetes_ODSC_Prediction_Drifted.csv
│   │   └── 10k_diabetes_ODSC_Training.csv
│   ├── Flask_App                   # Flask app for prediction via API endpoint
│   │   └── python_model
│   │       ├── __init__.py
│   │       ├── custom_model.pickle
│   │       ├── inference_model_scoring.py
│   │       ├── server
│   │       │   ├── __init__.py
│   │       │   ├── app.py
│   │       │   ├── app1.py
│   │       │   └── frontend
│   │       │       ├── static
│   │       │       │   └── styles
│   │       │       │       └── layout.css
│   │       │       └── templates
│   │       │           ├── __pycache__
│   │       │           │   └── blueprints.cpython-37.pyc
│   │       │           ├── apis
│   │       │           │   └── PredictPatientReadmissionScore.html
│   │       │           ├── blueprints.py
│   │       │           ├── includes
│   │       │           │   └── _formhelpers.html
│   │       │           └── layout.html
│   │       └── start_server.sh
│   ├── Notebook          # Jupyter Notebook/Python files for building the models
│   │   ├── ODSC_Readmission_LogisticRegression.ipynb
│   │   ├── ODSC_Readmission_LogisticRegression.py
│   │   ├── ODSC_Readmission_Random_Forest_Grid_Search.ipynb
│   │   └── ODSC_Readmission_Random_Forest_Grid_Search.py
│   └── Prediction        # Jupyter Notebook for predicion via DataRobot and Flask app
│       ├── DataRobot
│       │   └── DataRobot_V1_API.ipynb
│       └── Flask
│           └── ODSC_Prediction_Flask.ipynb
├── Dockerfile            # Dockerfile for the hands-on training enviroment
├── LICENSE
└── README.md

```

## 3. How To Use Jupyter Notebooks
Copy/paste this URL into your browser when you connect for the first time,


    to login with a token:
        http://localhost:8890/?token=<your token>