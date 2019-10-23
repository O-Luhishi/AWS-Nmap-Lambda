#!/usr/bin/env bash
export VIRTUALENV=".venv"
export ZIP_FILE="network-mapper-lambda-1.0.0.zip"
export PYTHON_VERSION="python3.6"
export TMP_FILE="tmp_deployment_folder"

# Zip Dependencies from virtualenv and root folder
mkdir ${TMP_FILE}
#pip install -r requirements.txt -t ${TMP_FILE}
cp -r vioft_network_mapper.py res/ ${TMP_FILE}
cd ${TMP_FILE}; zip -r ../${ZIP_FILE} *; cd ../
rm -rf ${TMP_FILE}


