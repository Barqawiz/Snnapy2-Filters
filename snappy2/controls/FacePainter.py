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
from snappy2.utils import Constants
from snappy2.utils.Utility import Utility
import PIL.Image as Image


class FacePainter:
    """
    Draw overlay images above faces using key points
        - draw overlay
        - draw glasses
        - draw mustache
        - draw hat
        - draw ears
        - draw key points


    Developed by: github.com/barqawiz
    """
    def __init__(self, image, key_properties):
        self.image = image
        self.key_properties = key_properties

    def draw_overlay(self, img_overlay, position=Constants.pos_eyes, x_margin_m=25,
                        y_margin_m=10, x_slide_m=0, y_slide_m=0, width_increase_p=0, extra_angle_m=0):
        """
        Draw overlay image above the detected face based on the received position
        :param img_overlay:
        :param position:
        :param x_margin_m: if the face is big, this parameter slide the overlay based on value and increase size of image
        :param y_margin_m: slide the overlay to up
        :param x_slide_m: extra slide for x positive or negative without increase size
        :param y_slide_m: extra slide for y positive or negative
        :param width_increase_p: percentage of increase in the width of overlay (smi supported in this version)
        :param extra_angle_m add extra value to rotation, positive or negative
        :return:
        """

        x_margin_m = abs(x_margin_m)
        for face in self.key_properties:
            x_axis = face['keys_x']
            y_axis = face['keys_y']
            face_y = face['face_y']
            face_w = face['face_w']
            face_h = face['face_w']
            # reset params
            x_margin = x_margin_m
            y_margin = y_margin_m
            x_slide = x_slide_m
            y_slide = y_slide_m
            extra_angle = extra_angle_m

            sx = None
            sy = None
            if position == Constants.pos_eyes:

                # common fixing values
                # space_to_eye = y_axis[9] - face_y
                x_margin += int((x_axis[6] - x_axis[8]) * 0.33)

                # size change
                target_width = int(x_axis[7] - x_axis[9]) + x_margin  # + extra margin (left and right)

                percent_increase = int(target_width * width_increase_p)
                target_width += percent_increase

                overlay_width = int(img_overlay.size[0])
                change_ratio = (target_width / overlay_width)

                target_width = int(img_overlay.size[0] * change_ratio)
                target_height = int(img_overlay.size[1] * change_ratio)

                # angle change
                angle = Utility.calc_angle(x_axis, y_axis) + extra_angle

                # prepare draw sun glasses params
                draw_height, draw_width = img_overlay.size
                sm = int(x_margin / 2) + int(percent_increase/2)
                sx = int(x_axis[9]) - sm
                sy = int(y_axis[9]) - y_margin
                sx += x_slide

                # transform overlay image
                img_overlay = img_overlay.resize((target_width, target_height), Image.ANTIALIAS)
                img_overlay = img_overlay.rotate(angle, resample=Image.BICUBIC, expand=True)

                if angle > 4:
                    if abs(y_axis[9] - y_axis[7]) > 10:
                        # slide a little
                        sx = sx - sm

            elif position == Constants.pos_must:

                # common fixing values
                space_to_mouth = y_axis[13] - y_axis[10]
                # print(space_to_mouth)
                if space_to_mouth >= 36:
                    y_margin += int(space_to_mouth * 0.2)
                elif space_to_mouth >= 32:
                    y_margin += int(space_to_mouth * 0.1)
                else:
                    y_margin += int(space_to_mouth * 0.05)
                #
                # size change
                target_width = int(x_axis[11] - x_axis[12]) + x_margin  # + extra margin (left and right)
                overlay_width = int(img_overlay.size[0])
                change_ratio = (target_width / overlay_width)

                target_width = int(img_overlay.size[0] * change_ratio)
                target_height = int(img_overlay.size[1] * change_ratio)

                # angle change
                angle = Utility.calc_angle(x_axis, y_axis) + extra_angle

                # prepare draw sun glasses params
                draw_height, draw_width = img_overlay.size
                sm = int(x_margin / 2)
                sx = int(x_axis[10]) - int(target_width/2) + x_slide
                sy = int(y_axis[10]) + y_margin

                # transform overlay image
                img_overlay = img_overlay.resize((target_width, target_height), Image.ANTIALIAS)
                img_overlay = img_overlay.rotate(angle, resample=Image.BICUBIC, expand=True)

            elif position == Constants.pos_ears:

                # common fixing values
                # space_to_eye = y_axis[9] - face_y
                x_margin += int(x_axis[6] - x_axis[8])

                # size change
                target_width = int(x_axis[7] - x_axis[9]) + x_margin  # + extra margin (left and right)
                overlay_width = int(img_overlay.size[0])
                change_ratio = (target_width / overlay_width)

                target_width = int(img_overlay.size[0] * change_ratio)
                target_height = int(img_overlay.size[1] * change_ratio)
                y_margin += int(target_height * 0.85)

                # angle change
                angle = Utility.calc_angle(x_axis, y_axis) + extra_angle

                # prepare draw sun glasses params
                draw_height, draw_width = img_overlay.size
                sm = int(x_margin / 2)
                sx = int(x_axis[9]) - sm
                sy = int(face_y) - y_margin
                sx += x_slide

                # transform overlay image
                img_overlay = img_overlay.resize((target_width, target_height), Image.ANTIALIAS)
                img_overlay = img_overlay.rotate(angle, resample=Image.BICUBIC, expand=True)

            elif position == Constants.pos_head:
                # common fixing values
                space_to_eye = int( (y_axis[9] - face_y)*0.3)
                x_margin += int(x_axis[6] - x_axis[8])*2

                # print(space_to_eye)

                # size change
                target_width = int(x_axis[7] - x_axis[9]) + x_margin  # + extra margin (left and right)
                overlay_width = int(img_overlay.size[0])
                change_ratio = (target_width / overlay_width)

                target_width = int(img_overlay.size[0] * change_ratio)
                target_height = int(img_overlay.size[1] * change_ratio)
                y_margin += int(target_height * 0.7)
                y_margin += int(space_to_eye * 0.9)

                # angle change
                angle = Utility.calc_angle(x_axis, y_axis) + extra_angle

                # prepare draw sun glasses params
                draw_height, draw_width = img_overlay.size
                sm = int(x_margin / 2)
                sx = int(x_axis[9]) - sm
                sy = int(face_y) - y_margin + y_slide
                sx += x_slide

                # transform overlay image
                img_overlay = img_overlay.resize((target_width, target_height), Image.ANTIALIAS)
                img_overlay = img_overlay.rotate(angle, resample=Image.BICUBIC, expand=True)
            else:
                raise Exception('unsupported position, check constants file for supported values')

            # draw overlay image
            if sx is not None and sy is not None:
                self.image.paste(img_overlay, (sx, sy), img_overlay)

    def draw_glasses(self, img_overlay, x_margin=5, y_margin=8, x_slide=0):
        """
        Draw overlay image on top the detected eyes

        :param img_overlay:
        :param x_margin: if the face is big, this parameter slide the overlay based on value and increase size of image
        :param y_margin: slide the overlay to up
        :param x_slide: extra slide for x positive or negative without increase size
        :return:
        """
        self.draw_overlay(img_overlay, position=Constants.pos_eyes, x_margin_m=x_margin, y_margin_m=y_margin,
                          x_slide_m=x_slide)

    def draw_mustache(self, img_overlay, x_margin=5, y_margin=5, x_slide=0):
        """
        Draw overlay image above the detected mouth

        :param img_overlay:
        :param x_margin: if the face is big, this parameter slide the overlay based on value and increase size of image
        :param y_margin: slide the overlay to up
        :param x_slide: extra slide for x positive or negative without increase size
        :return:
        """
        self.draw_overlay(img_overlay, position=Constants.pos_must, x_margin_m=x_margin, y_margin_m=y_margin,
                          x_slide_m=x_slide)

    def draw_hat(self, img_overlay, x_margin=25, y_margin=5, x_slide=-11, y_slide=0, width_increase_p=0, extra_angle=0):
        self.draw_overlay(img_overlay, position=Constants.pos_head, x_margin_m=x_margin, y_margin_m=y_margin,
                          x_slide_m=x_slide, y_slide_m=y_slide, width_increase_p=width_increase_p, extra_angle_m=extra_angle)

    def draw_ears(self, img_overlay, x_margin=4, y_margin=4, x_slide=0):
        self.draw_overlay(img_overlay, position=Constants.pos_ears, x_margin_m=x_margin, y_margin_m=y_margin,
                          x_slide_m=x_slide)

    def draw_key_points(self):
        if self.image is not None:
            print('not supported for this version, will be released in next versions')
