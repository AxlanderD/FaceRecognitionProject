# coding: utf-8
import mxnet as mx
from mtcnn.mtcnn_detector import MtcnnDetector
import cv2
import os
import  numpy as np
import  face_comm

model= os.path.abspath(face_comm.get_conf('mtcnn','model'))
def if_string_path(path):
    
    if isinstance(path,str):
        image_array = cv2.imread(path)
        return image_array
    else:
        return path

class Detect:
    def __init__(self):
        self.detector = MtcnnDetector(model_folder=model, ctx=mx.gpu(0), num_worker=4, accurate_landmark=False)
    def detect_face(self,image):
        image_array = if_string_path(image)
        results =self.detector.detect_face(image_array)
        boxes=[]
        faceKeyPoint = []
        if results is not None:
            #box框
            boxes=results[0]
            #人脸5个关键点
            points = results[1]
            for i in results[0]:
                faceKeyPoint = []
                for p in points:
                    for i in range(5):
                        faceKeyPoint.append([p[i], p[i + 5]])
        return {"boxes":boxes,"face_key_point":faceKeyPoint}


if __name__=='__main__':
    import  face_alignment
    pic='ImgDataSet/photo/9.jpg'
    detect = Detect()
    result = detect.detect_face(pic)
    print(result)
    pic = cv2.imread(pic)
    align_img_list = face_alignment.align_face(opic_array = pic,faceKeyPoint = result['face_key_point'])
    for i in align_img_list:
        cv2.imshow('Pic_Frame',i)
        cv2.waitKey(0)
