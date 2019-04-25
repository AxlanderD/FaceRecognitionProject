#coding=utf-8
import  face_comm
import  cv2
import  numpy as np
import  os
import  time
import  random
def align_face(opic_array,faceKeyPoint):
    #获得标准人脸
    #这里直接传入原来的图片矩阵
    # opic_array 传入的图片矩阵
    # faceKeyPoint 传入的五个关键点坐标
    fiveKeyPointsNum = int(len(faceKeyPoint)/5)
    #根据两个鼻子和眼睛进行3点对齐
    get_align_face = []
    #print('face count:',fiveKeyPointsNum)
    for num in range(0,fiveKeyPointsNum):
        num = num*5
        eye1 = faceKeyPoint[num]
        eye2 = faceKeyPoint[num+1]
        noise = faceKeyPoint[num+2]
        source_point = np.array(
            [eye1, eye2, noise], dtype=np.float32
        )

        eye1_noraml= [int(x) for x in face_comm.get_conf('alignment','left_eye').split(',')]
        eye2_noraml=[int(x) for x in face_comm.get_conf('alignment','right_eye').split(',')]
        noise_normal=[int(x) for x in face_comm.get_conf('alignment','noise').split(',')]
        #设置的人脸标准模型

        dst_point = np.array(
            [eye1_noraml,
            eye2_noraml,
            noise_normal],
            dtype=np.float32)

        tranform = cv2.getAffineTransform(source_point, dst_point)

        imagesize=tuple([int(x) for x in face_comm.get_conf('alignment','imgsize').split(',')])
        align_face_array = cv2.warpAffine(opic_array, tranform, imagesize)
        
        #是否将对齐人脸保存成图片
        '''
        ifSave = input('if save pic?[y/n]')
        if ifSave == 'y':
            new_image_save_path= os.path.abspath(face_comm.get_conf('alignment','aligment_face_dir'))
            new_image_save_path= new_image_save_path+'/'+'%d_%d.png'%(time.time(),random.randint(0,100))
            if cv2.imwrite(new_image_save_path,align_face_array):
                print('write success')       
            else:
                print('write failed') 
    '''
        get_align_face.append(align_face_array)
    return get_align_face
def save_align_pic(align_face_array_list):
    for align_face_array in align_face_array_list:
        new_image_save_path= os.path.abspath(face_comm.get_conf('alignment','aligment_face_dir'))
        new_image_save_path= new_image_save_path+'/'+'%d_%d.png'%(time.time(),random.randint(0,100))
        if cv2.imwrite(new_image_save_path,align_face_array):
            print('write success')       
        else:
            print('write failed') 
if __name__=='__main__':
    import  face_detect
    pic_dir='D:/Program File/Jupyter-NoteBook/Graduation Project/GraProject-release-0.3/imgData/'
    pic = ['img_2019-04-25_02-01-40.jpg','img_2019-04-25_02-01-53.jpg','img_2019-04-25_02-02-00.jpg','img_2019-04-25_02-02-12.jpg','img_2019-04-25_02-02-22.jpg','img_2019-04-25_02-03-50.jpg']
    detect = face_detect.Detect()
    for i in pic:
        result = detect.detect_face(pic_dir+i)
        if not result:
            print('Find face failed')
        else:
            print('boxes:',result['boxes'],'\nface_key_point:\n',result['face_key_point'],'\n')        
            pic = cv2.imread(pic_dir+i)
            align_face(pic,result['face_key_point'])
       