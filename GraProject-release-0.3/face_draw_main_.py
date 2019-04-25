import face_alignment
#这个是mxnet版本的mtcnn
import face_detect
import face_encoder
import face_annoy
#这个detector是facenet中的mtcnn
#import face_detect_tensor
import cv2
import time
import get_json_info   
from PIL import Image, ImageDraw, ImageFont
import numpy as np
#程序开始部分
print('程序开始加载检测模块...')
t1 = time.time()
faceDetect = face_detect.Detect()
#faceDetect = face_detect_tensor.Detection()
t2 = time.time()
print('加载耗时...%.2fs'%(t2-t1))
print('程序开始加载编码模块...')
t1 = time.time()
faceEncoder = face_encoder.Encoder()
t2 = time.time()
print('加载耗时...%.2fs'%(t2-t1))
print('程序开始加载索引模块...')
t1 = time.time()
annoy = face_annoy.face_annoy()
t2 = time.time()
print('加载耗时...%.2fs'%(t2-t1))
drawStyle_cost = []
drawChineseText_cost = []
search_name_cost = []
detect_face_cost = []
num = 0
#框的样式
def drawStyle(draw,left,top,right,bottom,left_right,top_bottom,color,thickline):
    #opencv的color （b，g，r）
    #print('人脸框开始绘制...')
    drawStyle_t1= time.time()
    cv2.line(draw,(left,top),(left+left_right,top),color,thickline)
    cv2.line(draw,(left+left_right*2,top),(right,top),color,thickline)
    cv2.line(draw,(left,top),(left,top+top_bottom),color,thickline)
    cv2.line(draw,(left,top+top_bottom*2),(left,bottom),color,thickline)
    cv2.line(draw,(left,bottom),(left+left_right,bottom),color,thickline)
    cv2.line(draw,(left+left_right*2,bottom),(right,bottom),color,thickline)
    cv2.line(draw,(right,top),(right,top+top_bottom),color,thickline)
    cv2.line(draw,(right,top+top_bottom*2),(right,bottom),color,thickline)
    drawStyle_t2 = time.time()
    global drawStyle_cost
    drawStyle_cost.append(drawStyle_t2-drawStyle_t1)
#显示中文字符
def drawChineseText(cv2img,font_size,point,text,check):
    #print('名字开始添加...')
    drawChineseText_t1= time.time()
    cv2Img = cv2.cvtColor(cv2img,cv2.COLOR_BGR2RGB)
    pilImg = Image.fromarray(cv2Img)
    draw_Img = ImageDraw.Draw(pilImg)
    text_color = (0,220,10)
    if font_size<15:
        font_size_Text = 15
    else:
        font_size_Text = font_size
    draw_Font = ImageFont.truetype(r"font/mtqianbi.ttf",font_size_Text, encoding="utf-8")
    if not check:
        text_color = (255,0,0)
    draw_Img.text(point,text,font = draw_Font,fill = text_color)
    draw = cv2.cvtColor(np.array(pilImg), cv2.COLOR_RGB2BGR)
    drawChineseText_t2 = time.time()
    global drawChineseText_cost
    drawChineseText_cost.append(drawChineseText_t2-drawChineseText_t1)
    return draw
#查询名字
def search_name(opic_array,find_face_result):
    #print('数据库查询对比开始...')
    #在这里之前做人脸检测，要不然后面还需要再加载一次MTCNN的模型，这里传入人脸检测的结果(结果为一个字典，其中包含box和faceKeyPoint)
    #人脸对齐
    search_name_t1= time.time()
    align_face_array_list = face_alignment.align_face(opic_array,find_face_result['face_key_point'])
    name = []
    for align_face_array in align_face_array_list:
        embeding = faceEncoder.generate_embedding(align_face_array)
        simlar_vector = annoy.query_vector(embeding)
        for sim_id in simlar_vector[0]:
            #print('sim:',sim_id)
            dist = faceEncoder.get_dist(embeding,annoy.annoy.get_item_vector(sim_id))
            #print('dist:',dist)
            if dist<0.95:
                get_name = get_json_info.get_person_name(sim_id)
                break
            get_name = 'Unknow'
        name.append(get_name)
    search_name_t2 = time.time()
    global search_name_cost
    search_name_cost.append(search_name_t2-search_name_t1)
    return name

#对于输入的图片进行检测
def face_box_draw(path):
    t1 = time.time()
    #print('开始进行人脸检测...')
    results = faceDetect.detect_face(path)
    #results = faceDetect.find_faces(path)
    if len(results['boxes'])==0:
        #print('抱歉没有发现人脸..')
        return False
    total_boxes = results['boxes']
    points = results['face_key_point']
    img = cv2.imread(path)
    get_name = search_name(img,results)
    draw = img.copy()
    for b in total_boxes:
        left = int(b[0])
        top = int(b[1])
        right = int(b[2])
        bottom = int(b[3])
        left_right = (right - left)//3
        top_bottom = (bottom - top)//3
        color = (0,205,0)
        thickline = 2
        font = cv2.FONT_ITALIC
        personInfo = get_name.pop(0)
        check =True
        if personInfo=='Unknow':
            color = (0,0,255)
            thickline = 3
            check = False
        #脸部画框
        drawStyle(draw,left,top,right,bottom,left_right,top_bottom,color,thickline)
        #因为OpenCV不支持中文，所以这里使用了PIL模块,转换成PIL图片然后添加中文再转换回来
        font_size = left_right//3
        draw = drawChineseText(draw,font_size,(left,top-font_size*1.2),personInfo,check)
    '''
    #画5个特征点
    for p in points:
        cv2.circle(draw,(p[0],p[1]), 1, (0, 0, 255), 2)'''

    cv2.namedWindow('Pic_Frame'+path,0)
    cv2.resize(draw,(0,0),fx=0.5, fy=0.5)
    cv2.imshow('Pic_Frame'+path, draw)
    #t2 =time.time()
    #print('运算时间开销为 %.2fs'%(t2-t1))
    cv2.waitKey(0)

def face_box_draw_video(model):
    if model == 'camera':
        cameraUser = input('cameraUser:')
        cameraPwd = input('cameraPwd:')
        cameraIP = input('ip:')
        video = 'http://%s:%s@%s:8081/'%(cameraUser,cameraPwd,cameraIP)
    elif model == 'video':
        video = input('video_path:')
    process_this_frame = 0
    FPS = []
    video_capture = cv2.VideoCapture(video)
    if video_capture.isOpened():
        print('Option start...')
        total_boxes =[]
        points =[]
    else:
        print('Option failed...')
        return
    
    while True:
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        start = time.time()
        #每5帧进行一次检测
        if process_this_frame%2==0:
            #这句话对图像进行人脸检测
            time_detect = time.time()
            results =faceDetect.detect_face(small_frame)
            #results = faceDetect.find_faces(small_frame)
            time_detect_2 = time.time()
            detect_face_cost.append(time_detect_2 -time_detect)
            if len(results['boxes'])>0 :
                total_boxes = results['boxes']
                points = results['face_key_point']
                get_name = search_name(small_frame,results)
                if len(total_boxes)>5:
                    #人脸数目大于5的时候才显示数目
                    print('人脸数目(>5时):%d\n'%len(points))
            else:
                total_boxes = []
                points = []
                get_name = []
        for b in total_boxes:
            left =4*int(b[0])
            top = 4*int(b[1])
            right = 4*int(b[2])
            bottom = 4*int(b[3])
            left_right = (right - left)//3
            top_bottom = (bottom - top)//3
            color = (0,205,0)
            thickline = 2
            font = cv2.FONT_ITALIC
            #if len(get_name)>0:
            personInfo = get_name.pop(0)
            #else:
            #    personInfo ='Unknow'
            check =True
            if personInfo=='Unknow':
                color = (0,0,255)
                thickline = 3
                check = False
            drawStyle(frame,left,top,right,bottom,left_right,top_bottom,color,thickline)
            font_size = left_right//3
            frame = drawChineseText(frame,font_size,(left,top-font_size*1.2),personInfo,check)
        process_this_frame =  process_this_frame + 1
        #计算帧率 主要是利用getTickCount()记录当前时间，以时钟周期计//和getTickFrequency()//时钟周期
        
        end = time.time()
        FPS.append(end-start)
        fpsInfo = 'FPS:'
        fpsInfo = fpsInfo + str(1.0/np.mean(FPS))[:4]
        font = cv2.FONT_ITALIC
        cv2.putText(frame,fpsInfo,(20,40),font,1.0,(0, 0, 255),2)
        
        cv2.namedWindow('Video_Frame',0)
        cv2.imshow('Video_Frame', frame)
        global num
        num = num + 1
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
    
    while True:
        path = input('请输入图片路径:')
        face_box_draw(path)
        key = input('是否继续检测[q键退出]?')
        if key == 'q':
            key = input('是否继续检测[q键退出!]?')
            if key =='q':
                break
        elif key =='n':
            continue
    
    model = input('请选择模型：“camera” or "video"\n')
    video_time1 = time.time()
    face_box_draw_video(model)
    video_time2 = time.time()
    print('drawStyle_cost平均时间：%.2fs'%np.mean(drawStyle_cost))
    print('drawChineseText平均时间：%.2fs'%np.mean(drawChineseText_cost))
    print('search_name_cost平均时间：%.2fs'%np.mean(search_name_cost))
    print('detect_face_cost平均时间：%.2fs'%np.mean(detect_face_cost))
    print('face_box_draw_video平均时间：%.2fs'%(float((video_time2-video_time1))/(num*1.0)))
    print('程序结束...')
    
