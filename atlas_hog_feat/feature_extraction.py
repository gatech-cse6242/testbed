from skimage.color import rgb2gray
from skimage.feature import hog
from skimage.io import imread
from skimage.transform import resize
from pickle import dump
from os import listdir
import numpy as np


if __name__ == '__main__':

    root_image_dir = '../images/'
    normalized_image_dir = '../normalized_images/'
    image_classes = listdir(root_image_dir)[:200]

    feature_set = {}

    percent_done = -1

    for i, image_class in enumerate(image_classes):
        
        percent = i*100 / len(image_classes)

        if percent != percent_done:
            percent_done = percent
            print '\t\t%d'%percent_done + '%'
        

        images = listdir(root_image_dir + image_class)
        feature_set[image_class] = []

        for image in images:
            image = rgb2gray(imread(root_image_dir + image_class + '/'+image))
            # preserve aspect ratio in rescale or warping ensues
            width, height = len(image), len(image[0])
            scaling_factor = 256.0 / min(width, height)
            new_width, new_height = int(width*scaling_factor), int(height*scaling_factor)
            resized_image = resize(image, (new_width, new_height))
            min_r, max_r = len(resized_image)/2 - 128 , len(resized_image)/2 + 128
            min_c, max_c = len(resized_image[0])/2 - 128 , len(resized_image)/2 + 128 
            cropped_image = resized_image[min_r:max_r, min_c:max_c]
            #TODO: sweep of feature parameters?
            features, _ = hog(cropped_image, orientations=8, pixels_per_cell=(16,16), cells_per_block=(1,1), visualise=True)

            feature_set[image_class].append((features, cropped_image))


    dump(feature_set, open('feature_set.pickle', 'w'))
