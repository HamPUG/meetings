# Redis application

## Setup

virtualenv -p /usr/bin/python3 venv
./venv/bin/pip install wai.tflite_model_maker

## Train model

./venv/bin/tmm-ic-train --images data/ --num_epochs 5 --output output/

## Use model

./venv/bin/tmm-ic-predict-redis --model ./output/model.tflite --labels ./output/labels.txt --redis_in images --redis_out predictions --verbose

./venv/bin/python predict.py
