import pickle
import os
import cv2
import numpy as np
import tensorflow as tf
from scipy import misc
import face_net.src.facenet as facenet
import  face_comm
import time

np.set_printoptions(suppress=True)
gpu_memory_fraction = 0.3
facenet_model_checkpoint = os.path.abspath(face_comm.get_conf('facedetect','model'))

class Encoder:
    def __init__(self):
        start=time.time()
        self.sess = tf.Session(config=tf.ConfigProto(log_device_placement=False))
        with self.sess.as_default():
            facenet.load_model(facenet_model_checkpoint)
        end = time.time()
        print ('faceNet Model loading finised,cost: %ds'%((end-start)))

    def generate_embedding(self,align_face_array):
        #这里直接传入align_face图像矩阵
        # Get input and output tensors
        images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
        embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
        phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
        if align_face_array.shape[1]>160:
            align_face_array = cv2.resize(align_face_array,(160,160))
        prewhiten_face = facenet.prewhiten(align_face_array)
        # Run forward pass to calculate embeddings
        feed_dict = {images_placeholder: [prewhiten_face], phase_train_placeholder: False}
        return self.sess.run(embeddings, feed_dict=feed_dict)[0]

    def get_dist(self,em1,em2):
        return np.sqrt(np.sum(np.square(np.subtract(em1,em2))))

if __name__=='__main__':
    import  face_alignment
    import face_detect
    encoder = Encoder()
    #faceDetector = face_detect.Detect()
    dirplace = 'D:/Program File/Jupyter-NoteBook/Graduation Project/Example/t_faceproject_2/alignface/'
    pic1='1555032085_62.png'
    pic2=[  '1555032085_90.png','1555032085_76.png','1555032086_48.png',\
            '1555032492_97.png','1555032592_69.png','1554966993_58.png',\
            '1555032085_4.png','1554966775_71.png','1554966930_78.png',\
            '1554966858_22.png','1554966429_6.png']
    for pic in pic2:
        em = encoder.generate_embedding(cv2.imread(dirplace+pic))
        print('dim',len(em))
    '''
        核心流程：
            1.MTCNN检测人脸
            2.通过OpenCV对检测到的人脸进行剪切对齐
            3.通过faceNet进行人脸特征编码得到embeding1
            4.取出annoy中的人脸特征得到特征embeding2
            5.通过dist计算embeding1和embeding2的欧氏空间距离判断是否是同一个人
            6.如果判断是同一个人则返回id，根据id在数据库中进行索引
    '''
    '''
    import face_annoy
    import get_json_info
    annoy = face_annoy.face_annoy()
    t1 = time.time()
    path = [r'ImgDataSet\photo\61.jpg',r'ImgDataSet\photo\58.jpg',r'ImgDataSet\photo\40.jpg',r'ImgDataSet\photo\54.jpg',r'ImgDataSet\photo\78.jpg',r'ImgDataSet\photo\75.jpg',\
        r'ImgDataSet\photo\41.jpg',r'ImgDataSet\photo\65.jpg'
        ]
    
    #align_face_array_list = []
    #align_face_array_list.append(opic_array)
    #annoy中进行索引 取得最相近的点然后进行特征向量欧式距离计算
    name =[]
    for i in path:
        find_face_result = faceDetector.detect_face(i)
        opic_array = cv2.imread(i)
        align_face_array_list = face_alignment.align_face(opic_array,find_face_result['face_key_point'])
        for align_face_array in align_face_array_list:
            embeding = encoder.generate_embedding(align_face_array)
            simlar_vector = annoy.query_vector(embeding)
            for sim_id in simlar_vector[0]:
                print('sim:',sim_id)
                dist = encoder.get_dist(embeding,annoy.annoy.get_item_vector(sim_id))
                print('dist:',dist)
                if dist<0.9:
                    get_name = get_json_info.get_person_name(sim_id)
                    break
                get_name = 'Unknow'
            name.append(get_name)
    print('search_name:',name)    
    t2 =time.time()
    print('time cost:%.2f'%(t2-t1))'''
    
    

