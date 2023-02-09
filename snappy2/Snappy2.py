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
import sys
sys.path.insert(0, '..')

# from utils.Constants import Constants, Overlays
from snappy2.utils import Constants, Overlays
from snappy2.controls import Detector
from snappy2.controls import FacePainter
import PIL.Image as Image
from PIL import ImageFont, ImageDraw
import cv2
import numpy as np
import os


class Snappy2:

    def __init__(self):
        self.detector = Detector()
        self.base_folder = os.path.dirname(__file__)

    def load_image(self, image_path):
        return Image.open(image_path)

    def draw_overlay_path(self, path_human, path_overlay, draw_pos=Constants.pos_eyes):#
        """
        Detect faces in photos and draw overlay images on it

        :param path_human: image file path
        :param path_overlay: image file path
        :param draw_pos: send one of following eyes | ears | head | mustache
        :return:
        """
        img_human = Image.open(path_human)
        img_overlay = Image.open(path_overlay)

        return self.draw_overlay(img_human, img_overlay, draw_pos=draw_pos)

    def draw_overlay(self, img_human, img_overlay, draw_pos=Constants.pos_eyes):
        """
        Detect faces in photos and draw overlay images on it

        :param img_human: PIL Image
        :param img_overlay: PIL Image
        :param draw_pos: send one of following eyes | ears | head | mustache
        :return:
        """
        image_gray = cv2.cvtColor(np.array(img_human), cv2.COLOR_BGR2GRAY)
        face_properties = self.detector.detect_faces(image_gray)
        key_properties = self.detector.detect_key_points(face_properties)

        face_painter = FacePainter(img_human, key_properties)

        if draw_pos == Constants.pos_eyes:
            face_painter.draw_glasses(img_overlay)
        elif draw_pos == Constants.pos_must:
            face_painter.draw_mustache(img_overlay)
        elif draw_pos == Constants.pos_ears:
            face_painter.draw_ears(img_overlay)
        elif draw_pos == Constants.pos_head:
            face_painter.draw_hat(img_overlay)
        elif draw_pos == Constants.pos_noise:
            print('not supported in this version')
        elif draw_pos == Constants.pos_lips:
            print('not supported in this version')

    def set_glasses(self, img_human, gls_index=0):
        """
        draw glasses on face

        :param img_human:
        :param gls_index: position for value inside (utils.Constants.Overlays.draw_glasses) array
        :return:
        """
        assert gls_index < len(Overlays.draw_glasses), 'Error mustache position'
        overlay_name = Overlays.draw_glasses[gls_index]

        file_overlay = os.path.join(self.base_folder, 'resource/images/overlay/' + overlay_name)

        assert os.path.exists(file_overlay), 'Overlay image does not exist'
        img_overlay = Image.open(file_overlay).convert("RGBA")

        image_gray = cv2.cvtColor(np.array(img_human), cv2.COLOR_BGR2GRAY)
        face_properties = self.detector.detect_faces(image_gray)
        key_properties = self.detector.detect_key_points(face_properties)

        face_painter = FacePainter(img_human, key_properties)
        face_painter.draw_glasses(img_overlay)

    def set_mustache(self, img_human, mus_index=0):
        """
        draw mustache on face

        :param img_human:
        :param mus_index: position for value inside (utils.Constants.Overlays.draw_mus) array
        :return:
        """
        assert mus_index < len(Overlays.draw_mus), 'Error mustache position'
        overlay_name = Overlays.draw_mus[mus_index]

        file_overlay = os.path.join(self.base_folder, 'resource/images/overlay/'+overlay_name)

        assert os.path.exists(file_overlay), 'Overlay image does not exist'
        img_overlay = Image.open(file_overlay).convert("RGBA")

        image_gray = cv2.cvtColor(np.array(img_human), cv2.COLOR_BGR2GRAY)
        face_properties = self.detector.detect_faces(image_gray)
        key_properties = self.detector.detect_key_points(face_properties)

        face_painter = FacePainter(img_human, key_properties)
        if mus_index == 1 or mus_index == 2:
            face_painter.draw_mustache(img_overlay, x_margin=30, x_slide=-3)
        else:
            face_painter.draw_mustache(img_overlay)

    def set_hat(self, img_human, hat_index=0, y_slide=0, width_increase_p=0):
        """
        draw hat on head

        :param img_human:
        :param hat_index:
        :param y_slide: slide the hat up or down based on the value
        :param width_increase_p percentage of increase in overlay width
        :return:
        """
        assert hat_index < len(Overlays.draw_hat), 'Error mustache position'
        overlay_name = Overlays.draw_hat[hat_index]

        file_overlay = os.path.join(self.base_folder, 'resource/images/overlay/' + overlay_name)

        assert os.path.exists(file_overlay), 'Overlay image does not exist'
        img_overlay = Image.open(file_overlay).convert("RGBA")

        image_gray = cv2.cvtColor(np.array(img_human), cv2.COLOR_BGR2GRAY)
        face_properties = self.detector.detect_faces(image_gray)
        key_properties = self.detector.detect_key_points(face_properties)

        face_painter = FacePainter(img_human, key_properties)
        if hat_index == 1:
            face_painter.draw_hat(img_overlay, x_slide=-24, y_slide=y_slide, width_increase_p=width_increase_p)
        else:
            face_painter.draw_hat(img_overlay, y_slide=y_slide, width_increase_p=width_increase_p)

    def set_ears(self, img_human, ea_index=0):
        """
        draw ears on head
        :param img_human:
        :param ea_index:
        :return:
        """

        assert ea_index < len(Overlays.draw_ears), 'Error mustache position'
        overlay_name = Overlays.draw_ears[ea_index]

        file_overlay = os.path.join(self.base_folder, 'resource/images/overlay/' + overlay_name)

        assert os.path.exists(file_overlay), 'Overlay image does not exist'
        img_overlay = Image.open(file_overlay).convert("RGBA")

        image_gray = cv2.cvtColor(np.array(img_human), cv2.COLOR_BGR2GRAY)
        face_properties = self.detector.detect_faces(image_gray)
        key_properties = self.detector.detect_key_points(face_properties)

        face_painter = FacePainter(img_human, key_properties)
        face_painter.draw_ears(img_overlay)

    def set_text(self, object_image, draw_text, text_size, text_fill='#FFFFFF',
                 v_position='bottom', h_position='center'):
        """
        draw text of received image

        :param object_image:
        :param draw_text:
        :param text_size:
        :param text_fill: HTML color code
        :param v_position: bottom OR top
        :param h_position: left OR right OR center
        :return:
        """
        assert v_position in ['bottom','top', 'center'], "received position value not supported." +\
                                                         "\nValue should be bottom or top"
        assert h_position in ['center', 'left', 'right'], "received position value not supported." +\
                                                          "\nValue should be bottom or top"

        if len(draw_text) > 0:

            font = ImageFont.truetype(os.path.join(self.base_folder, "resource/font/Asap-Bold.ttf"), text_size)
            canvas = ImageDraw.Draw(object_image)

            y_margin = 4
            x_margin = 8
            f_w, f_h = canvas.textsize(draw_text, font)
            im_w, im_h = object_image.size
            x = int(im_w/2)-int(f_w/2)
            if h_position == 'left':
                x = x_margin
            elif h_position == 'right':
                x = int(im_w) - int(f_w) - x_margin
            if v_position == 'bottom':
                y = im_h-f_h-y_margin
            elif v_position == 'top':
                y = 0 + y_margin
            elif v_position == 'center':
                y = int(im_h/2) - int(f_h/2)

            canvas.text((x,y), draw_text, font=font, fill=text_fill)
