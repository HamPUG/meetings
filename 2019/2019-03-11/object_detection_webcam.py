######## Picamera Object Detection Using Tensorflow Classifier #########
#
# Date: 4/15/18
# Description: 
# This program uses a TensorFlow classifier to perform object detection.
# It loads the classifier uses it to perform object detection on a Picamera feed.
# It draws boxes and scores around the objects of interest in each frame from
# the Picamera. It also can be used with a webcam by adding "--usbcam"
# when executing this script from the terminal.

## Some of the code is copied from Google's example at
## https://github.com/tensorflow/models/blob/master/research/object_detection/object_detection_tutorial.ipynb

## and some is copied from Dat Tran's example at
## https://github.com/datitran/object_detector_app/blob/master/object_detection_app.py

## and some code from Evan Juras

## and modifications for making it work with IP webcam by Peter Reutemann


# Import packages
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
import requests
import base64
import time

# Set up camera constants
#IM_WIDTH = 1280
#IM_HEIGHT = 720
IM_WIDTH = 640    #Use smaller resolution for
IM_HEIGHT = 480   #slightly faster framerate

# This is needed since the working directory is the object_detection folder.
sys.path.append('..')

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

# Name of the directory containing the object detection module we're using
model_name = 'ssdlite_mobilenet_v2_coco_2018_05_09'

# Grab path to current working directory
cwd_path = os.getcwd()

# Path to frozen detection graph .pb file, which contains the model that is used
# for object detection.
path_to_chkpt = os.path.join(cwd_path,model_name,'frozen_inference_graph.pb')

# Path to label map file
path_to_labels = os.path.join(cwd_path,'data','mscoco_label_map.pbtxt')

# Number of classes the object detector can identify
num_classes = 90

## Load the label map.
# Label maps map indices to category names, so that when the convolution
# network predicts `5`, we know that this corresponds to `airplane`.
# Here we use internal utility functions, but anything that returns a
# dictionary mapping integers to appropriate string labels would be fine
print("loading labels:", path_to_labels)
label_map = label_map_util.load_labelmap(path_to_labels)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=num_classes, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

all_labels = []
for category in categories:
    all_labels.append(category["name"] + "/" + str(category["id"]))
all_labels.sort()
print("labels:", all_labels)

# Load the Tensorflow model into memory.
print("loading model:", model_name)
detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(path_to_chkpt, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)


# Define input and output tensors (i.e. data) for the object detection classifier

# Input tensor is the image
image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

# Output tensors are the detection boxes, scores, and classes
# Each box represents a part of the image where a particular object was detected
detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

# Each score represents level of confidence for each of the objects.
# The score is shown on the result image, together with the class label.
detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

# Number of objects detected
num_detections = detection_graph.get_tensor_by_name('num_detections:0')

# webcam URL
url = "http://192.168.1.103/image.jpg"
url_user = "image"
url_pw = "image"
print("url:", url)

# capture interval
capture_interval = 1
print("capture interval:", capture_interval)

# output dir
output_dir = "/home/pi/tf/output"

# labels to monitor
monitored_labels = ["person", "cat", "dog"]
monitored_label_ids = []
for category in categories:
    if category["name"] in monitored_labels:
        monitored_label_ids.append(category["id"])
print("monitored labels:", monitored_labels)
print("monitored label ids:", monitored_label_ids)

threshold_labels = {"person": 0.5}
threshold_label_ids = {}
threshold_default = 0.5
for category in categories:
    if category["name"] in monitored_labels:
        id = monitored_label_ids[monitored_labels.index(category["name"])]
        if category["name"] in threshold_labels:
            threshold_label_ids[id] = threshold_labels[category["name"]]
        else:
            threshold_label_ids[id] = threshold_default
print("threshold per label id:", threshold_label_ids)

while(True):

    # get frame
    r = requests.get(url, auth=(url_user, url_pw))
    img_array = np.array(bytearray(r.content), dtype=np.uint8)
    frame = cv2.imdecode(img_array, -1)
    frame_expanded = np.expand_dims(frame, axis=0)

    # Perform the actual detection by running the model with the image as input
    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    ts = time.strftime("%Y%m%d-%H%M%S")
    match = False
    print("\n" + ts)
    for id in threshold_label_ids:
        print(scores[0, id])
        if scores[0, id] >= threshold_label_ids[id]:
            match = True
            print(monitored_labels[monitored_label_ids.index(id)], scores[0, id])

    if match:
        if output_dir is not None:
            cv2.imwrite(output_dir + "/" + ts + ".jpg", frame)

    time.sleep(capture_interval)

