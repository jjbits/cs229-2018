import os
import time
import numpy as np
from PIL import Image
import glob
import cv2


class BaseCamera:

    def run_threaded(self):
        return self.frame


class PiCamera(BaseCamera):
    def __init__(self, resolution=(120, 160), framerate=20):
        from picamera.array import PiRGBArray
        from picamera import PiCamera
        resolution = (resolution[1], resolution[0])
        # initialize the camera and stream
        self.camera = PiCamera()  # PiCamera gets resolution (height, width)
        self.camera.resolution = resolution
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=resolution)
        self.stream = self.camera.capture_continuous(self.rawCapture,
                                                     format="rgb",
                                                     use_video_port=True)

        # initialize the frame and the variable used to indicate
        # if the thread should be stopped
        self.frame = None
        self.on = True

        print('PiCamera loaded.. .warming camera')
        time.sleep(2)

    def run(self):
        f = next(self.stream)
        frame = f.array
        self.rawCapture.truncate(0)
        return frame

    def filter_image(self, image):
        hsv_image = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)
        sensitivity = 51
        lower_white = np.array([0,0,255-sensitivity])
        upper_white = np.array([255,sensitivity,255])
        lower_yellow = np.array([18,102,204], np.uint8)
        upper_yellow = np.array([25,255,255], np.uint8)
        white_mask = cv2.inRange(hsv_image, lower_white, upper_white)
        yellow_mask = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
        filtered_image = cv2.bitwise_and(image, image, mask=white_mask+yellow_mask)
        return filtered_image

    def update(self):
        # keep looping infinitely until the thread is stopped
        for f in self.stream:
            # grab the frame from the stream and clear the stream in
            # preparation for the next frame
            #image = cv2.cvtColor(f.array, cv2.COLOR_BGR2GRAY)
            #image = cv2.Canny(f.array, 50, 150)
            #self.frame = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            #self.frame = self.filter_image(f.array)
            self.frame = f.array
            self.rawCapture.truncate(0)

            # if the thread indicator variable is set, stop the thread
            if not self.on:
                break

    def shutdown(self):
        # indicate that the thread should be stopped
        self.on = False
        print('stoping PiCamera')
        time.sleep(.5)
        self.stream.close()
        self.rawCapture.close()
        self.camera.close()
