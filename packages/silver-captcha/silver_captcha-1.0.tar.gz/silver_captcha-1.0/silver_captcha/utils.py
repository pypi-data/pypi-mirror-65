import cv2
import numpy as np
import random
import math


def add_gaussian_noise(img):

    width,height,channel = img.shape

    #Gaussian distribution parameters
    mean = 0
    var = 0.1
    sigma = var ** 0.5

    # gaussian = np.random.random((width,height,1)).astype(np.float32)
    # gaussian = np.concatenate((gaussian,gaussian,gaussian), axis=2)
    # gaussian_noise_img = cv2.addWeighted(img,0.75,0.25*gaussian,0.25,0)
    #
    # gaussian_noise_img = np.array(gaussian_noise_img, dtype=np.float32)

    gaussian = np.random.normal(mean,sigma,(width,height,channel))
    gaussian = gaussian.reshape(width,height,channel)
    gaussian_noise_img = img + gaussian

    return gaussian_noise_img

def add_salt_pepper_noise(img):
    """:arg img - Opencv image
    """

    width,height,channel = img.shape
    sp_noise_img = np.copy(img)
    control_val1 = 0.004
    control_val2 = 0.5

    #Adding salt noise
    salt_qty = np.ceil(control_val1 * img.size * control_val2)
    selected_coordinates = [np.random.randint(0,i-1,int(salt_qty)) for i in img.shape]
    sp_noise_img[tuple(selected_coordinates)] = 1

    #Adding pepper noise
    pepper_qty = np.ceil(control_val1 * img.size *(1 - control_val2))
    selected_coordinates = [np.random.randint(0, i - 1, int(pepper_qty)) for i in img.shape]
    sp_noise_img[tuple(selected_coordinates)] = 0

    return sp_noise_img

def add_poisson_noise(img):
    values = len(np.unique(img))
    values = 2** np.ceil(np.log2(values))
    noisy_img = np.random.poisson(img * values) / float(values)

    return noisy_img

def draw_random_line_on_image(img):

    width, height,channel = img.shape

    """Calculating coordinates randomly within the image area"""
    x1 = int(width * random.uniform(0 ,0.1))
    y1 = int(height * random.uniform(0 ,1))
    x2 = int(width * random.uniform(0.9 ,1))
    y2 = int(height * random.uniform(0 ,1))

    """Calculating the line width randomly considering the image area as a parameter"""
    line_width = round((width * height) ** 0.5 * 2.284e-2)

    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return img

def warp_images(img,warp_type):
    width, height, channel = img.shape
    warped_img = np.zeros(img.shape, dtype=img.dtype)
    #warped_img = img.copy

    if "vertical" in warp_type:
        for i in range(width):
            for j in range(height):
                dx = int(25.0 * math.sin(2 * 3.14 * i / 180))
                dy = 0
                if j + dx < width:
                    warped_img[i, j] = img[i, (j + dx) % height]
                else:
                    warped_img[i, j] = 0
    elif "horizontal" in warp_type:
        for i in range(width):
            for j in range(height):
                dx = 0
                dy = int(16.0 * math.sin(2 * 3.14 * j / 150))
                if i + dy < width:
                    warped_img[i, j] = img[(i + dy) % width, j]
                else:
                    warped_img[i, j] = 0
    elif "both" in warp_type:
        for i in range(width):
            for j in range(height):
                dx = int(20.0 * math.sin(2 * 3.14 * i / 150))
                dy = int(20.0 * math.cos(2 * 3.14 * j / 150))
                if i + dy < width and j + dx < height:
                    warped_img[i, j] = img[(i + dy) % width, (j + dx) % height]
                else:
                    warped_img[i, j] = 0

    return warped_img

def write_text_character(char,img, coord):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, char, coord, font, 3, (0, 255, 0), 2, cv2.LINE_AA)
    return img






