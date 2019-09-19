import argparse
import os
import PIL.Image as Image
from Snappy2 import Snappy2

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--demo", help="Demo number", type=float)

DEFAULT_INDEX = 2

human_image = Image.open('resource/images/test_images/side_face.jpg')

def draw_glasses():
    print('0- draw_glasses')

    # create snnapy object to draw overlay
    snappy2 = Snappy2()
    snappy2.set_glasses(human_image, gls_index=0)
    human_image.show()


def draw_mustache():
    print('1- draw_mustache')

    # create snnapy object to draw overlay
    snappy2 = Snappy2()
    snappy2.set_mustache(human_image, mus_index=0)
    human_image.show()


def draw_hat():
    print('2- draw_hat')

    # create snnapy object to draw overlay
    snappy2 = Snappy2()
    snappy2.set_hat(human_image, hat_index=0, y_slide=0, width_increase_p=0.25)

    human_image.show()


def draw_ears():
    print('3- draw_ears')

    # create snnapy object to draw overlay
    snappy2 = Snappy2()
    snappy2.set_ears(human_image, ea_index=2)
    human_image.show()


def draw_text():
    print('4- draw_text')

    # create snnapy object to draw overlay
    snappy2 = Snappy2()
    snappy2.set_text(human_image, 'Snappy2', 60, v_position='bottom')
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
