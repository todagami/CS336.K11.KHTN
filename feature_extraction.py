import cv2
import numpy as np
import scipy
#from scipy.misc import imread
from scipy.misc.pilutil import imread
import pickle
import random
import os
import matplotlib.pyplot as plt
import scipy.spatial
# Feature extractor
def extract_features(image, vector_size=32):
    try:
        # Using KAZE, cause SIFT, ORB and other was moved to additional module
        # which is adding addtional pain during install
        alg = cv2.KAZE_create()
        # Dinding image keypoints
        kps = alg.detect(image)
        # Getting first 32 of them. 
        # Number of keypoints is varies depend on image size and color pallet
        # Sorting them based on keypoint response value(bigger is better)
        #kps = sorted(kps, key=lambda x: -x.response)[:vector_size]
        # computing descriptors vector
        kps, dsc = alg.compute(image, kps)
        # Flatten all of them in one big vector - our feature vector
        dsc = dsc.flatten() 

        # Making descriptor of same size
        # Descriptor vector size is 64
        needed_size = (vector_size * 64)
        if dsc.size < needed_size:
            # if we have less the 32 descriptors then just adding zeros at the
            # end of our feature vector
            dsc = np.concatenate([dsc, np.zeros(needed_size - dsc.size)])
    except cv2.error as e:
        print ('Error: ', e)
        return None

    return dsc


import glob
def batch_extractor():
    output = open("index.csv", "w")
        # use glob to grab the image paths and loop over them
    for imagePath in glob.glob("/content/resources/images/oxbuild_images" + "/*.jpg"):
      # extract the image ID (i.e. the unique filename) from the image
      # path and load the image itself
      imageID = imagePath[imagePath.rfind("/") + 1:]
      print ('Extracting features from image %s' % imageID)
      image = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)

      # describe the image
      features = extract_features(image)

      # write the features to file
      features = [str(f) for f in features]
      output.write("%s,%s\n" % (imageID, ",".join(features)))

    # close the index file
    output.close()

#batch_extractor()