#!/bin/bash

# Configurate project by installing all necessary requirements.


echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Installing all necessary requirements!"
echo '----------------------------------------------------------------------------------------------------------'
echo

requirements_file="requirements.txt"
pip install -r $requirements_file

echo
echo '----------------------------------------------------------------------------------------------------------'
echo "Finished installing requirements!"
echo '----------------------------------------------------------------------------------------------------------'
echo
