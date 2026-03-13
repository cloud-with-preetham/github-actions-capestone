#!/bin/bash

python app.py &
sleep 5
curl http://localhost:5000/health
