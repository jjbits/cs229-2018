import numpy as np
import cv2
from matplotlib import pyplot as plt
 
img = cv2.imread('bad.jpg',0)
 
# create a CLAHE object (Arguments are optional).
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
 
cv2.imwrite('clahe_2.jpg',cl1)
