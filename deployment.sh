#!/bin/bash

cd ~/Deployment
if [ -z "$VIRTUAL_ENV" ]; then
    source deployment/bin/activate
else
    echo "Virtual environment is already active."
fi
PORT=8501
PID=$(lsof -ti :$PORT)

if [ ! -z "$PID" ]; then
    # echo "Port $PORT is already in use. Opening http://localhost:8501..."
    xdg-open "http://localhost:8501" &>/dev/null &
    exit 0
fi

streamlit run streamlit.py
