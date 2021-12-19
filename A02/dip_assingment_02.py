# -*- coding: utf-8 -*-
"""DIP_Assingment_02.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K1dNA7-ux2EkPNom691F1SEzGeWNUlTy

###Muhammad Saad Hassan
###P176137 - 7A
###Digital Image Processing
###Assignment No. 02
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import math
from google.colab import drive
drive.mount('/content/drive')


class Image:

    def __init__(self, image_file):

        # read image to array
        self.image = Image.open(image_file)
        self.image.show()

        # self.modified_image = Image.open(image_file)

        # convert image into greyscale
        self.image_grey = self.image.convert("L")
        self.image_grey.show()

        self.dimension = self.image_grey.size
        print("Dimension = ", self.dimension)

    # Question no: 1
    def Sobel_edgeProfile(self, image):

        img_vals = np.array(image)
        final_img_vals = np.zeros((self.dimension[1], self.dimension[0]))
        for u in range(len(img_vals)):
            for v in range(len(img_vals[0])):
                if u == 0:
                    y_prev = 0
                else:
                    y_prev = img_vals[u-1][v]
                if u == len(img_vals) - 1:
                    y_forw = 0
                else:
                    y_forw = img_vals[u+1][v]
                if v == 0:
                    x_prev = 0
                else:
                    x_prev = img_vals[u][v-1]
                if v == len(img_vals[0]) - 1:
                    x_forw = 0
                else:
                    x_forw = img_vals[u][v+1]

                center = 4*(img_vals[u][v])
                final_val = x_prev + x_forw + y_prev + y_forw - center
                final_img_vals[u][v] = final_val

        image = Image.fromarray(final_img_vals)
        return image

    # Question no: 2

    def laplacian_of_Gaussian(self, sigma):
        """First we will calculate the Gaussian lowpass filter to smooth the image and then apply the Laplacian to get the required filter"""

        img_vals = np.array(self.image_grey)
        final_img_vals = np.zeros((self.dimension[1], self.dimension[0]))

        # Gaussian Low pass filter
        for u in range(len(img_vals)):
            for v in range(len(img_vals[0])):

                final_val = round(
                    math.exp((-(img_vals[u][v]**2) / (sigma**2))))
                final_img_vals[u][v] = final_val

        img = Image.fromarray(final_img_vals, "L")
        img = self.laplacianEdgeProfile(img)
        img.show()

    # Question no: 3

    def signal_to_Noise_Ratio(self, image_file):
        original_img_vals = np.array(self.image_grey)

        # read image to array
        noisy_img = Image.open(image_file)

        # convert image into greyscale
        image_grey = noisy_img.convert("L")
        noisy_img_vals = np.array(image_grey)

        sum_of_noise_vals = 0
        for u in range(len(noisy_img_vals)):
            for v in range(len(noisy_img_vals[0])):
                sum_of_noise_vals += (noisy_img_vals[u][v]**2)

        diff_of_noisy_original = 0
        for u in range(len(noisy_img_vals)):
            for v in range(len(noisy_img_vals[0])):
                diff_of_noisy_original += (
                    (original_img_vals[u][v] - noisy_img_vals[u][v]) ** 2)

        SNR = sum_of_noise_vals // diff_of_noisy_original
        return SNR

    # Question no: 4

    def frequency_domain(self):
        original_img_vals = np.array(self.image_grey)
        magnitude_img_vals = np.zeros(
            (self.dimension[1], self.dimension[0]))
        phase_img_vals = np.zeros((self.dimension[1], self.dimension[0]))

        Mth = len(magnitude_img_vals)
        Nth = len(magnitude_img_vals[0])
        for m in range(len(magnitude_img_vals)):
            for n in range(len(magnitude_img_vals[0])):
                img_val = 0
                real_val = 0
                for x in range(len(original_img_vals)):
                    for y in range(len(original_img_vals[0])):
                        power_val = ((x * m) / Mth) + ((y*n) / Nth)
                        res = f"{(math.e**(math.pi*2j*power_val)) * original_img_vals[x][y]:.2f}"
                        r_val = 1
                        if res[0] == '-':
                            res = res[1:]
                            r_val *= -1
                        res = res.split("-")
                        if len(res) > 1:
                            real_val += r_val * float(res[0])
                            img_val += -1*float(res[1][:-1])

                        else:
                            res = res[0].split("+")
                            real_val += r_val*float(res[0])
                            img_val += float(res[1][:-1])

                magnitude_img_vals[m][n] = (
                    (real_val ** 2) + (img_val ** 2)) ** 0.5
                try:
                    phase_img_vals[m][n] = math.atan(
                        abs(real_val / img_val))
                except ZeroDivisionError as error:
                    phase_img_vals[m][n] = math.radians(90)

        img = Image.fromarray(magnitude_img_vals)
        img.show()

    # Question no: 5

    def lowPass_filter(self, cutOff_dist=5):
        image_vals = np.array(self.image_grey)
        Mth = len(image_vals)
        Nth = len(image_vals[0])
        filter_img_vals = np.zeros((self.dimension[1], self.dimension[0]))
        for u in range(len(filter_img_vals)):
            for v in range(len(filter_img_vals[0])):
                dist = ((((u - Mth) / 2) ** 2) + (((v - Nth) / 2) ** 2)) ** 0.5
                if dist <= cutOff_dist:
                    filter_img_vals[u][v] = 1
                else:
                    filter_img_vals[u][v] = 0

    # Question no: 6

    def highPass_filter(self, cutOff_dist=5):
        img_vals = np.array(self.image_grey)
        Mth = len(img_vals)
        Nth = len(img_vals[0])
        filter_img_vals = np.zeros((self.dimension[1], self.dimension[0]))
        for u in range(len(filter_img_vals)):
            for v in range(len(filter_img_vals[0])):
                dist = ((((u - Mth) / 2) ** 2) + (((v - Nth) / 2) ** 2)) ** 0.5
                if dist <= cutOff_dist:
                    filter_img_vals[u][v] = 0
                else:
                    filter_img_vals[u][v] = 1


if __name__ == "__main__":
    # load input image
    image = "/content/drive/MyDrive/DIP/A02/data/Fig0338(a)(blurry_moon).tif"

    # creating object of Image class
    instance = Image(image)

    # Question no: 1
    instance.Sobel_edgeProfile(image)

    # Question no: 2
    instance.laplacianOfGaussian(10)

    # Question no: 3
    instance.signalToNoiseRatio(image)

    # Question no: 4
    instance.frequency_domain()

    # Question no: 5
    instance.lowPass_filter()

    # Question no: 6
    instance.highPass_filter()


### ______ The END ______  ###
