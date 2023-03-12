# based on: 
# https://gradio.app/image-classification-in-tensorflow/
# requires tensorflow to be installed
#   pip install tensorflow

import tensorflow as tf
import requests
import gradio as gr
import os

# load pretraind model
inception_net = tf.keras.applications.MobileNetV2()

# Download human-readable labels for ImageNet if not on disk.
labels_file = "./labels.txt"
if not os.path.exists(labels_file):
    response = requests.get("https://git.io/JJkYN")
    with open(labels_file, "w") as fp:
        fp.write(response.text)
with open(labels_file, "r") as fp:
    labels = [x.strip() for x in fp.readlines()]


def classify_image(inp):
  inp = inp.reshape((-1, 224, 224, 3))
  inp = tf.keras.applications.mobilenet_v2.preprocess_input(inp)
  prediction = inception_net.predict(inp).flatten()
  confidences = {labels[i]: float(prediction[i]) for i in range(1000)}
  return confidences



gr.Interface(fn=classify_image, 
             inputs=gr.Image(shape=(224, 224)),
             outputs=gr.Label(num_top_classes=3),
             examples=["banana.jpg", "car.jpg"]).launch()

