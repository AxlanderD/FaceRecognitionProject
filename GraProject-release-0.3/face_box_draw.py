
import cv2
import time
import get_json_info as getInfo  
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import face_handler 
import face_detect
#这个模块因为face_detect模块中的MTCNN模型加载的时候使用了进程池 会重复复制进程（在windows的环境表现很奇怪）。但是定义的函数不会重复执行。因此
#对于其他模块的加载和初始化应该放在函数中，否则函数外会重复初始化加载
get_align_pic = face_handler.get_align_pic
query_face = face_handler.query_face
faceDetect = face_detect.Detect()
print('face_box_draw 开始执行')

#脸部框的样式
def drawStyle(draw,left,top,right,bottom,left_right,top_bottom,color):
        #opencv的color （b，g，r）
        print('face_box_draw.drawStyle 开始执行')
        thickline = 1
        cv2.line(draw,(left,top),(left+left_right,top),color,thickline)
        cv2.line(draw,(left+left_right*2,top),(right,top),color,thickline)
        cv2.line(draw,(left,top),(left,top+top_bottom),color,thickline)
        cv2.line(draw,(left,top+top_bottom*2),(left,bottom),color,thickline)
        cv2.line(draw,(left,bottom),(left+left_right,bottom),color,thickline)
        cv2.line(draw,(left+left_right*2,bottom),(right,bottom),color,thickline)
        cv2.line(draw,(right,top),(right,top+top_bottom),color,thickline)
        cv2.line(draw,(right,top+top_bottom*2),(right,bottom),color,thickline)
#显示中文字符
def drawChineseText(cv2img,font_size,point,text):
    print('face_box_draw.drawChineseText 开始执行')
    cv2Img = cv2.cvtColor(cv2img,cv2.COLOR_BGR2RGB)
    pilImg = Image.fromarray(cv2Img)
    draw_Img = ImageDraw.Draw(pilImg)
    if font_size<15:
        font_size_Text = 15
    else:
        font_size_Text = font_size
    draw_Font = ImageFont.truetype(r"font/mtqianbi.ttf",font_size_Text, encoding="utf-8")
    draw_Img.text(point,text,(0,255,127),font = draw_Font)
    draw = cv2.cvtColor(np.array(pilImg), cv2.COLOR_RGB2BGR)
    return draw

def search_name(img_array,faces_get_result):
    print('face_box_draw.search_name 开始执行')
    print('faces_get_result',faces_get_result)
    #在这里之前做人脸检测，要不然后面还需要再加载一次MTCNN的模型，这里传入人脸检测的结果
    align_faces_t1 = time.time()
    align_faces = get_align_pic(img_array,faces_get_result)
    align_faces_t2 = time.time()
    print('align_faces_cost:%.2fs'%(align_faces_t2-align_faces_t1))
    get_id = []
    get_name = []
    for face in align_faces:
        query_face_t1 = time.time()
        get_id_dis = query_face(face)
        query_face_t2 = time.time()
        print('query_face_cost:%.2fs'%(query_face_t2-query_face_t1))
        query_id = get_id_dis[0]
        query_dis = get_id_dis[1]
        #dis小于1.06时可以认为是同一个人，也可以设置的小一些
        if min(query_dis)<1.06:
            index = query_dis.index(min(query_dis))
            print('min_dis index_id:',query_id[index])
            print('min_dis',query_dis)
            get_id.append(query_id[index])
        else:
            index = query_dis.index(min(query_dis))
            print('min_dis index_id:',query_id[index])
            print('min_dis',query_dis)
            print('Can not find this person')
            get_id.append(0)
    for id in get_id:
        get_name.append(getInfo.get_person_name(id))
    return get_name

def face_box_draw(path):
    print('face_box_draw.face_box_draw 开始执行')
    t1 = time.time()    
    img = cv2.imread(path)
    #返回脸部坐标和5个特征点的坐标
    results = faceDetect.detect_face(path,True)
    if results is None:
        print('No Result Return')
        return
    total_boxes = results['boxes']
    points = results['face_key_point']
    nc = time.time()
    #get_name = search_name(img,results)
    nc_2 = time.time()
    print('get_name cost %.2fs'%(nc_2-nc))
    #get_name = ['unknow']*19
    draw = img.copy()
    for b in total_boxes:
        left = int(b[0])
        top = int(b[1])
        right = int(b[2])
        bottom = int(b[3])
        left_right = (right - left)//3
        top_bottom = (bottom - top)//3
        color = (0,205,0)
        font = cv2.FONT_ITALIC
        personInfo = 'un'
        #脸部画框
        drawStyle(draw,left,top,right,bottom,left_right,top_bottom,color)
        #因为OpenCV不支持中文，所以这里使用了PIL模块,转换成PIL图片然后添加中文再转换回来
        font_size = left_right//3
        draw = drawChineseText(draw,font_size,(left,top-font_size*1.2),personInfo)

    for p in points:
        cv2.circle(draw,(p[0],p[1]), 1, (0, 0, 255), 2)

    cv2.namedWindow('Pic_Frame'+path,0)
    cv2.resize(draw, (0, 0), fx=0.25, fy=0.25)
    cv2.imshow('Pic_Frame'+path, draw)
    t2 = time.time()
    print('Total cost time:%.2f'%(t2-t1))
    cv2.waitKey(0)
    #cv2.destroyWindow('Pic_Frame')
    


def face_box_draw_video(model):
    if model == 'camera':
        cameraUser = input('cameraUser')
        cameraPwd = input('cameraPwd')
        cameraIP = input('ip')
        video = 'http://%s:%s@%s:8081/'%(cameraUser,cameraPwd,cameraIP)
    elif model == 'video':
        video = input('video_path:')
    else:
        print('Model Error')
        return
    process_this_frame = 0
    getFace = False
    drawKeyPoint =False
    video_capture = cv2.VideoCapture(video)
    if video_capture.isOpened():
        print('Option start...')
        total_boxes =[]
        points =[]
    else:
        print('Option failed...')
        return
    #这个必须放在while循环外面否则每次都会进行初始化并加载模型，拖低帧率
    faceDetect = face_detect.Detect()
    while True:
        #fps显示实时帧率
        start = time.time()
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        #每5帧进行一次检测
        if process_this_frame%5==0:
            #这句话对图像进行人脸检测
            results =faceDetect.detect_face(small_frame,False)
            if results is not False:
                total_boxes = results['boxes']
                points = results['face_key_point']
                if len(total_boxes)>5:
                    #人脸数目大于5的时候才显示数目
                    print('faceNum:\n',len(points))
            else:
                total_boxes = []
                points = []
            process_this_frame = 0
        
        for b in total_boxes:
            left =4*int(b[0])
            top = 4*int(b[1])
            right = 4*int(b[2])
            bottom = 4*int(b[3])
            left_right = (right - left)//3
            top_bottom = (bottom - top)//3
            color = (0,205,0)
            font = cv2.FONT_ITALIC
            id = 1 
            personInfo = getInfo.get_person_name(id)
            cv2.putText(frame,personInfo,(left,top-15),font,1.5,(127,255,0),2)
            drawStyle(frame,left,top,right,bottom,left_right,top_bottom,color)
    
        process_this_frame =  process_this_frame + 1
        #计算帧率 主要是利用getTickCount()记录当前时间，以时钟周期计//和getTickFrequency()//时钟周期
        end = time.time()
        fpsInfo = 'FPS:%.2f'%(1.0/(end-start))
        font = cv2.FONT_ITALIC
        cv2.putText(frame,fpsInfo,(20,40),font,1.0,(0, 0, 255),2)
        cv2.namedWindow('Video_Frame',0)
        cv2.imshow('Video_Frame', frame)

        key = cv2.waitKey(5)
        if key ==27:
            print('Exit...')
            break
        if key == ord(' '):
            localTime = time.localtime()
            timeUnix = time.strftime('%Y-%m-%d_%H-%M-%S',localTime)
            filename = 'imgData\\img_%s.jpg'%timeUnix
            if cv2.imwrite(filename,frame):
                print('Save Img Already')
            else:
                print('Sorry your option failed')
        
    video_capture.release()
    cv2.destroyAllWindows()



    

if __name__=='__main__':  
    path = [r'D:\Program File\Jupyter-NoteBook\Graduation Project\Example\t_faceproject_2\alignface\1554966993_99.png']
    #faceDetect = face_detect.Detect()
    print('启动人脸检测器')
    for i in path:
        face_box_draw(path=i)
 
   
