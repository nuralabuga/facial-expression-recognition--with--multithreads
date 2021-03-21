import cv2
from model import FacialExpressionModel
import numpy as np
import threading, time
import queue
import logging
import sys
from memory_profiler import profile

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

BUFFER_SIZE = 700
qbuffer = queue.Queue(BUFFER_SIZE)

class ProducerThread(threading.Thread):
    def __init__(self, name):
        super(ProducerThread,self).__init__()
        self.name = name
        self._stop = threading.Event() 
  
    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet()
    
    @profile
    def run(self):                        
        while True:
            if self.stopped(): 
                return                          
            ret, fr = rgb.read()
            if not qbuffer.full(): 
                if ret==True:                
                    qbuffer.put(fr) 
                    logging.debug('ProducerThread ' + str(qbuffer.qsize()) + ' items in queue')           
        return

class ConsumerThread(threading.Thread):
    def __init__(self, name):
        super(ConsumerThread,self).__init__()
        self.name = name
        self._stop = threading.Event() 
        return

    def stop(self): 
        self._stop.set() 
  
    def stopped(self): 
        return self._stop.isSet()        
    
    @profile
    def run(self):
        f=0
        while True:
            if self.stopped(): 
                return        
            if not qbuffer.empty():
                f+=1
                fr = qbuffer.get()
                if f%5==1:
                    gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
                    faces = facec.detectMultiScale(gray_fr, 1.3, 5) 
                    for (x, y, w, h) in faces:
                        fc = gray_fr[y:y+h, x:x+w]
                        
                        roi = cv2.resize(fc, (48, 48))
                        norm = np.zeros((48,48))
                        roi = cv2.normalize(roi,  norm, 0, 255, cv2.NORM_MINMAX)
                        pred = cnn.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
                        cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
                        cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)
                
                    cv2.imshow("emotion_win",fr)
                    cv2.waitKey(1)
                    logging.debug('ConsumerThread ' + str(qbuffer.qsize()) + ' items in queue') 

                    #out.write(fr)                    
        return
        


if __name__ == '__main__':

    rgb = cv2.VideoCapture(0)
    facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    font = cv2.FONT_HERSHEY_SIMPLEX
    cnn = FacialExpressionModel("face_model.json", "face_model.h5")
    #fourcc = cv2.VideoWriter_fourcc(*'XVID')
    #out = cv2.VideoWriter('output.avi',fourcc,float(5), (640,480))    

    t1 = ProducerThread(name='producer')
    t2 = ConsumerThread(name='consumer')

    t1.start()   
    t2.start()
   
    time.sleep( 30 )
    t1.stop() 
    t2.stop() 
    
    


 
