import pickle
import os
import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
import face_net.src.facenet as facenet
import face_net.src.align.detect_face
import  face_comm
import time
from PIL import Image, ImageDraw, ImageFont
np.set_printoptions(suppress=True)
gpu_memory_fraction = 0.65
facenet_model_checkpoint = os.path.abspath(face_comm.get_conf('facedetect','model'))

def if_string_path(image_path):
    
    if isinstance(image_path,str):
        if os.path.exists(image_path):
            image_array = misc.imread(os.path.expanduser(image_path), mode='RGB')
            return image_array
        return None
    else:
        return image_path

class Face:
    def __init__(self):
        self.name = None
        self.bounding_box = None
        self.image = None
        self.container_image = None
        self.embedding = None

class Detection:
    # face detection parameters
    minsize = 20  # minimum size of face
    threshold = [0.6, 0.7, 0.7]  # three steps's threshold
    factor = 0.709  # scale factor

    def __init__(self, face_crop_size=160, face_crop_margin=32):
        self.pnet, self.rnet, self.onet = self._setup_mtcnn()
        self.face_crop_size = face_crop_size
        self.face_crop_margin = face_crop_margin

    def _setup_mtcnn(self):
        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                return face_net.src.align.detect_face.create_mtcnn(sess, None)

    def find_faces(self, image):
        image = if_string_path(image)
        #faces = []
        if image is not None:
            bounding_boxes,total_points= face_net.src.align.detect_face.detect_face(image, self.minsize,self.pnet, self.rnet, self.onet,self.threshold, self.factor)
        else:
            bounding_boxes = []
            total_points = []
        key_points = []
        for i in bounding_boxes:
            faceKeyPoint = []
            for i in range(5):
                faceKeyPoint.append([np.array(total_points[i]).astype(float), np.array(total_points[i + 5]).astype(float)])
            key_points.append(faceKeyPoint)
        '''
        for bb in bounding_boxes:
            face = Face()
            face.container_image = image
            face.bounding_box = np.zeros(4, dtype=np.int32)

            img_size = np.asarray(image.shape)[0:2]
            #np.maximum（x，y）逐位取最大值
            face.bounding_box[0] = np.maximum(bb[0] - self.face_crop_margin / 2, 0)
            face.bounding_box[1] = np.maximum(bb[1] - self.face_crop_margin / 2, 0)
            face.bounding_box[2] = np.minimum(bb[2] + self.face_crop_margin / 2, img_size[1])
            face.bounding_box[3] = np.minimum(bb[3] + self.face_crop_margin / 2, img_size[0])
            cropped = image[face.bounding_box[1]:face.bounding_box[3], face.bounding_box[0]:face.bounding_box[2], :]
            face.image = misc.imresize(cropped, (self.face_crop_size, self.face_crop_size), interp='bilinear')
            faces.append(face)
            misc.imsave('find_face',face.img)'''
        #return faces[0]
        return {"boxes":bounding_boxes,"face_key_point":key_points}