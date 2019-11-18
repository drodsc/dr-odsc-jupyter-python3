#!/bin/sh
cd /DataRobot_ODSC/Flask_App/python_model/ || exit 1
#export PYTHONPATH=/opt/code
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
export FLASK_APP=server.app
export FLASK_ENV=development
export MODULE_NAME=inference_model_scoring
export CLASS_NAME=CustomInferenceModel
python3 -m flask run --host=0.0.0.0 --port 8080
