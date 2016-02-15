from os import listdir
from shutil import copyfile

if __name__ == '__main__':
    image_source_dir = 'isic_images_cropped_256/'
    images = listdir(image_source_dir)
    ground_truth = 'isic_ground_truth.csv'
    dest_dir = 'isic/'
    lines = open(ground_truth).read().split('\n')

    data_labels = {}

    for line in lines:
        foo = line.split(',')
        if len(foo) > 1:
            image, label = foo

            if label:

                copyfile(image_source_dir + image, dest_dir+label+'/'+image+'.jpg' )
        
