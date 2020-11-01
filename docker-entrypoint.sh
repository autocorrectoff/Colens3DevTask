#!/bin/sh

#  Move the default configuration file out of the way. 
mv ./config/e_config.py ./config/unused.e_config.py
mv ./config/e_config_docker.py ./config/e_config.py

python3.7 -u rest.py