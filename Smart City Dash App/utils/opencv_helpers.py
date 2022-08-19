#!/usr/bin/env python
import cv2
#from imageai.Detection import ObjectDetection
#import os
#import urllib.request
#from keras import backend as K

class VideoCamera(object):
    def __init__(self, src):
        self.video = cv2.VideoCapture(src)
#        self.video.set(cv2.CAP_PROP_FPS, 30)

    def __del__(self):
        self.video.release()
    
    def detectCars(self):
#      cascade = cv2.CascadeClassifier('./static/cars.xml')
#      
#      if self.video.isOpened():
#          rval , frame = self.video.read()
#      else:
#          rval = False
#          
#      while rval:
#        
#          rval, frame = self.video.read()
#          frameHeight, frameWidth, fdepth = frame.shape
#          
#          # Resize
#          frame = cv2.resize(frame, ( 600,  400 ))
#          gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#            
#          # car detection.
#          cars = cascade.detectMultiScale(gray, 1.3, 3)
#          for (x, y, w, h) in cars:
#              cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

          rval , frame = self.video.read()
          ret, jpeg = cv2.imencode('.jpg', frame)
#          cv2.waitKey(50)
          return jpeg.tobytes()
#      return []
      
def gen(camera):
    try:
        while True:
            frame = camera.detectCars()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except:
        pass

#def process_img(input_img, output_img):
#    detector = ObjectDetection()
#    detector.setModelTypeAsRetinaNet()
#    detector.setModelPath( "./model/resnet50_coco_best_v2.0.1.h5")
#    detector.loadModel()
#    custom_objects = detector.CustomObjects(car=True, motorcycle= True, bus = True, truck = True)
#    
#    detections = detector.detectCustomObjectsFromImage(custom_objects = custom_objects,
#                                                       input_image = input_img,
#                                                       output_image_path = output_img,
#                                                       minimum_percentage_probability = 40,
#                                                       display_percentage_probability = False)
#    img = cv2.imread(output_img)
#    cv2.putText(img, 'Count: ' + str(len(detections)) , (20, 60), cv2.FONT_HERSHEY_DUPLEX, 1.5, (255, 0, 0), 2, cv2.LINE_AA)
#    cv2.imwrite(output_img,img) 
#    K.clear_session()
#    try:
#        for eachObject in detections:
#            print(eachObject["name"] , " : " , eachObject["percentage_probability"] )
#    except:
#        pass
