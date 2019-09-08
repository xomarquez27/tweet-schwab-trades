#!/bin/bash

cd ~/Desktop/Python/Schwab_Tweets/  # Replace with path to your project folder.

#  Needed for imports not in standard library but installed in virtual environment to work.

source gmail_env/bin/activate  # Replace with path to your virtual environment

python3 tweet_schwab.py  # Name of main .py file

deactivate  # Deactivate virtual environment
