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
import numpy as np
import math

class Utility:

    @staticmethod
    def calc_angle(x_axis, y_axis):
        angle1 = math.degrees(math.atan2(y_axis[8] - y_axis[9], x_axis[8] - x_axis[9]))

        return -angle1

    @staticmethod
    def reverse_nn_normalization(y_predict):
        return y_predict * 48 + 48
