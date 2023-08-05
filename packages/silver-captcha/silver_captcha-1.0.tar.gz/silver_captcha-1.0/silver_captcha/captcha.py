import random,string
from . import utils
import numpy as np



class SilverCaptcha:

    text = None
    height = 200
    width = 500
    warp_dict = {0:"horizontal",1:"vertical",2:"both"}
    text_length = 6

    def __init__(self):
        """Generating random text"""
        self.text = ''.join(random.choices(string.ascii_uppercase+string.digits+string.ascii_lowercase,k=self.text_length))

    def generate_captcha(self):

        """Creating white canvas"""
        canvas = np.zeros((self.height,self.width,3),np.uint8)
        canvas.fill(255)

        """Writing text """
        coord_x = 30
        coord_y = 100
        for i,char in enumerate(self.text):
            canvas = utils.write_text_character(char, canvas, (coord_x, coord_y))
            #canvas = utils.warp_images(canvas,self.warp_dict.get(random.randrange(0,3,1)))
            coord_x += 40


        """Generating noise"""
        canvas = utils.add_salt_pepper_noise(canvas)

        """Warping image"""
        canvas = utils.warp_images(canvas, "horizontal")

        """Drawing line"""
        canvas = utils.draw_random_line_on_image(canvas)
        canvas = utils.draw_random_line_on_image(canvas)
        canvas = utils.draw_random_line_on_image(canvas)
        canvas = utils.draw_random_line_on_image(canvas)
        canvas = utils.draw_random_line_on_image(canvas)

        canvas = canvas[0:self.height-80,0:self.width-80]

        return canvas

