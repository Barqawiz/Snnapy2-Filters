Detector.py
Today
9:41 PM

You edited an item
Text
Detector.py
9:31 PM

You edited an item
Text
Detector.py
9:17 PM

You edited an item
Text
Detector.py
8:09 PM

You edited an item
Text
Detector.py
7:44 PM

You edited an item
Text
Detector.py
7:12 PM

You uploaded an item
Text
Detector.py
"""
License
-------
    The MIT License (MIT)

    Copyright (c) 2018 Snappy2 Project

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

Created on Sat Dec 16 22:46:28 2017

@author: Ahmad Barqawi
@Source: Github.com/Barqawiz
"""

import cv2
from keras.models import load_model
import numpy as np
from utils.Utility import Utility
import os


class Detector:
    """
    Common class to detect areas of interest from images

    Developed by: github.com/barqawiz
    """
    def __init__(self):
        base_folder = os.path.dirname(__file__)
        #self.face_cascade = cv2.CascadeClassifier(
        #    os.path.join(base_folder,'../resource/haarcascades/haarcascade_frontalface_default.xml'))
        
        DNN = "CAFFE" ## TF/CAFFE
        if DNN == "CAFFE":
            modelFile = "./resource/models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
            configFile = "./resource/models/deploy.prototxt"
            self.net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
        else:
            modelFile = "./resource/models/opencv_face_detector_uint8.pb"
            configFile = "./resource/models/opencv_face_detector.pbtxt"
            self.net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
        
        self.model = load_model(os.path.join(base_folder,  '../resource/models/keras_cv_base_model_1_avg.h5'))

    def detect_faces(self, human_image):
        """
        Detect faces in image and return list of faces with related properties
        :param human_image: numpy array image
        :return: face_properties a list of dictionary with following information (face, loc, size)
        """
        face_properties = []
        conf_threshold = 0.5
        image_height, image_width, _ = human_image.shape
        print(human_image.shape)
        #faces = self.face_cascade.detectMultiScale(gray_human_image, 1.2, 7, minSize=(30, 30))
        #if len(faces) == 0:
        #    faces = self.face_cascade.detectMultiScale(gray_human_image, 1.1, 8, minSize=(30, 30))

        blob = cv2.dnn.blobFromImage(human_image, 1.0, (300, 300), [104, 117, 123], False, False)
 
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x = int(detections[0, 0, i, 3] * image_width)
                y = int(detections[0, 0, i, 4] * image_height)
                w = int(detections[0, 0, i, 5] * image_width) - x
                h = int(detections[0, 0, i, 6] * image_height) - y

                roi_image = human_image[y:y + h, x:x + w]
                face_properties.append({'face': roi_image, 'loc': (x, y), 'size': (w, h)})

        return face_properties

    def detect_key_points(self, face_properties, network_in_size=96):
        """
        Detect key points areas in the face using neural network.
            - key points for eyes, noise and mouth

        :param face_properties:
        :param network_in_size:
        :return: key_properties a list of dictionary with following information (keys_x, keys_y, face_index)
        """

        key_properties = []
        index = 0
        for face in face_properties:
            # 0- get face information
            roi_image = face['face']
            x,y = face['loc']
            w, h = face['size']

            # 1- pre process
            # prepare face image
            roi_image = cv2.resize(roi_image, (network_in_size, network_in_size))
            # scale pixel values to [0, 1]
            roi_image = roi_image / 255
            # reshape for netowork format
            roi_image = roi_image.reshape(roi_image.shape[0], roi_image.shape[1], 1)
            roi_image = np.array([roi_image])

            # 2- predict face key points
            y_predict = self.model.predict(roi_image)[0]
            # map to original coordinates values
            y_predict = Utility.reverse_nn_normalization(y_predict)

            # 3- extract information
            # get value within the original image
            x_axis = y_predict[0::2]
            y_axis = y_predict[1::2]
            x_scale_factor = (w / 96)
            y_scale_factor = (h / 96)
            x_axis = x_axis * x_scale_factor + x
            y_axis = y_axis * y_scale_factor + y

            key_properties.append({'keys_x': x_axis, 'keys_y': y_axis, 'face_x': x, 'face_y': y,
                                   'face_w': w, 'face_h': h, 'face_index': index})
            index += 1

        return key_properties
