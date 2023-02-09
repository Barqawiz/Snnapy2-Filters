import argparse
import os
import PIL.Image as Image
from snappy2 import Snappy2

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--demo", help="Demo number", type=float)

DEFAULT_INDEX = 2

snappy = Snappy2()
human_image = snappy.load_image('snappy2/resource/images/test_images/front_face.jpg')

def draw_glasses():
    print('0- draw_glasses')

    # draw overlay
    snappy.set_glasses(human_image, gls_index=0)
    human_image.show()


def draw_mustache():
    print('1- draw_mustache')

    # draw overlay
    snappy.set_mustache(human_image, mus_index=0)
    human_image.show()


def draw_hat():
    print('2- draw_hat')

    # draw overlay
    snappy.set_hat(human_image, hat_index=0, y_slide=0, width_increase_p=0.25)

    human_image.show()


def draw_ears():
    print('3- draw_ears')

    # draw overlay
    snappy.set_ears(human_image, ea_index=2)
    human_image.show()


def draw_text():
    print('4- draw_text')

    # draw overlay
    snappy.set_text(human_image, 'Snappy2', 60, v_position='bottom')
    human_image.show()


if __name__ == '__main__':

    args = parser.parse_args()

    demo = DEFAULT_INDEX if args.demo is None else args.demo

    if demo == 0:
        draw_glasses()
    elif demo == 1:
        draw_mustache()
    elif demo == 2:
        draw_hat()
    elif demo == 3:
        draw_ears()
    elif demo == 4:
        draw_text()
