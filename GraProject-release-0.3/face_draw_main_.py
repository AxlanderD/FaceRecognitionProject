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
import pyttsx3

class face_draw_main():
    def __init__(self):
        #程序开始部分
        print('程序开始加载检测模块...')
        t1 = time.time()
        self.faceDetect = face_detect.Detect()
        #faceDetect = face_detect_tensor.Detection()
        t2 = time.time()
        print('加载耗时...%.2fs'%(t2-t1))
        print('程序开始加载编码模块...')
        t1 = time.time()
        self.faceEncoder = face_encoder.Encoder()
        t2 = time.time()
        print('加载耗时...%.2fs'%(t2-t1))
        print('程序开始加载索引模块...')
        t1 = time.time()
        self.annoy = face_annoy.face_annoy()
        t2 = time.time()
        print('加载耗时...%.2fs'%(t2-t1))
        self.drawStyle_cost = []
        self.drawChineseText_cost = []
        self.search_name_cost = []
        self.detect_face_cost = []
        self.num = 0
        #检测到认识的人
        self.Friend  = []
        self.engine = pyttsx3.init(debug = True)
        
    #框的样式
    def drawStyle(self,draw,left,top,right,bottom,left_right,top_bottom,color,thickline):
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
        self.drawStyle_cost.append(drawStyle_t2-drawStyle_t1)
    #显示中文字符
    def drawChineseText(self,cv2img,font_size,point,text,check):
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
        self.drawChineseText_cost.append(drawChineseText_t2-drawChineseText_t1)
        return draw
    #查询名字
    def search_name(self,opic_array,find_face_result):
        #print('数据库查询对比开始...')
        #在这里之前做人脸检测，要不然后面还需要再加载一次MTCNN的模型，这里传入人脸检测的结果(结果为一个字典，其中包含box和faceKeyPoint)
        #人脸对齐
        search_name_t1= time.time()
        align_face_array_list = face_alignment.align_face(opic_array,find_face_result['face_key_point'])
        name = []
        count = 0
        for align_face_array in align_face_array_list:
            embeding = self.faceEncoder.generate_embedding(align_face_array)
            simlar_vector = self.annoy.query_vector(embeding)
            for sim_id in simlar_vector[0]:
                #print('sim:',sim_id)
                dist = self.faceEncoder.get_dist(embeding,self.annoy.annoy.get_item_vector(sim_id))
                if count == 0:
                    save_first_dist = dist
                count = count + 1
                #dist为识别距离
                if dist<0.75:
                    get_name = get_json_info.get_person_name(sim_id)
                    break
                get_name = 'Unknow'
            name.append((get_name,save_first_dist))
        search_name_t2 = time.time()
        self.search_name_cost.append(search_name_t2-search_name_t1)
        return name

    def AutoSound(self,name,loopNum,rate):
        '''
        控制音速和音量属性
        
        volume = engine.getProperty('volume')
        setrate = input('set rate:')
        setvolume = input('set Volume:')
        
        engine.setProperty('volume',volume+float(setvolume))
        '''
        rate = self.engine.getProperty('rate')
        self.engine.setProperty('rate',rate+float(rate))
        for i in range(loopNum):
            self.engine.say('注意')
            self.engine.say('检测到目标 %s'%name)
        self.engine.runAndWait()

    #对于输入的图片进行检测
    def face_box_draw(self,path,autoControl):
        autoCheck = autoControl[0]
        autoScreenShot = autoControl[2]
        autoSound = autoControl[3]
        SearchNameList = autoControl[4]
        savePath = autoControl[5]
        self.Friend =[]
        t1 = time.time()
        #print('开始进行人脸检测...')
        results = self.faceDetect.detect_face(path)
        #results = faceDetect.find_faces(path)
        if len(results['boxes'])==0:
            #print('抱歉没有发现人脸..')
            return False
        total_boxes = results['boxes']
        points = results['face_key_point']
        img = cv2.imread(path)
        get_name = self.search_name(img,results)
        draw = img.copy()
        if len(total_boxes)>0:
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
                personInfo_name = personInfo[0]
                personInfo_dist = personInfo[1]
                if personInfo_name != 'Unknow':
                    if personInfo_name in self.Friend:
                        pass
                    else:
                        self.Friend.append(personInfo_name)
                check =True
                if personInfo_name=='Unknow':
                    color = (0,0,255)
                    thickline = 3
                    check = False
                if autoCheck:
                    if personInfo_name in SearchNameList:
                        color = (0,215,255)
                #脸部画框
                self.drawStyle(draw,left,top,right,bottom,left_right,top_bottom,color,thickline)
                #因为OpenCV不支持中文，所以这里使用了PIL模块,转换成PIL图片然后添加中文再转换回来
                #co = '( %.2f,%.2f)'%((left+right)/2.0,(top+bottom)/2.0)
                font_size = left_right//3
                #cv2.putText(draw,co,(right,top-font_size),cv2.FONT_HERSHEY_SIMPLEX ,1,color,1)
                draw = self.drawChineseText(draw,font_size,(left,top-font_size*1.2),personInfo_name+'    dist:'+str(round(personInfo_dist,2)),check)
                if autoCheck:
                    if autoSound:
                        if personInfo_name in SearchNameList:
                            self.AutoSound(personInfo_name,3,0.00)
                    if autoScreenShot:
                        localTime = time.localtime()
                        timeUnix = time.strftime('%Y-%m-%d_%H-%M-%S',localTime)
                        filename = savePath.replace('/','\\')+'img_'+timeUnix+'.jpg'
                        print('\nfilename,savePath: %s %s '%(filename,savePath))
                        if cv2.imwrite(filename,draw):
                            print('截图保存成功，路径为 : %s'%filename)
                        else:
                            print('截图保存失败')


        '''
        #画5个特征点
        for p in points:
            cv2.circle(draw,(p[0],p[1]), 1, (0, 0, 255), 2)'''

        cv2.namedWindow('Pic_Frame'+path,0)
        cv2.resize(draw,(0,0),fx=0.5, fy=0.5)
        cv2.imshow('Pic_Frame'+path, draw)
        t2 =time.time()
        #print('运算时间开销为 %.2fs'%(t2-t1))
        cv2.waitKey(0)
        print('识别总人数为：%d'%len(results['boxes']))
        if len(self.Friend)>0:
            print('已识别的人名：',self.Friend)
        else:
            print('无识别人员')
        print('耗时：%.2fs'%(t2-t1))

    def face_box_draw_video(self,model,path,cameraUser,cameraPwd,cameraIP,autoControl):
        AutoCheck = autoControl[0]
        AutoStop = autoControl[1]
        AutoScreenShot = autoControl[2]
        AutoSound = autoControl[3]
        SearchNameList = autoControl[4]
        DefaultSavePath = autoControl[5]
        if model == 'camera':
            if cameraUser=='':
                video = 0
            else:
                video = 'http://%s:%s@%s:8081/'%(cameraUser,cameraPwd,cameraIP)
        elif model == 'video':
            video = path
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
        Update = False
        self.Friend =[]
        while True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            start = time.time()
            frame_copy = frame
            #每5帧进行一次检测
            if process_this_frame%4==0:
                #这句话对图像进行人脸检测
                time_detect = time.time()
                results =self.faceDetect.detect_face(small_frame)
                #results = faceDetect.find_faces(small_frame)
                time_detect_2 = time.time()
                self.detect_face_cost.append(time_detect_2 -time_detect)
                if len(results['boxes'])>0 :
                    total_boxes = results['boxes']
                    points = results['face_key_point']
                    get_name = self.search_name(small_frame,results)
                    if len(total_boxes)>5:
                        #人脸数目大于5的时候才显示数目
                        print('人脸数目(>5时):%d\n'%len(points))
                else:
                    total_boxes = []
                    points = []
                    get_name = []
            index = 0
            if len(total_boxes)>0:
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
                    personInfo = get_name[index]
                    personInfo_name,personInfo_dist = personInfo[0],personInfo[1]
                    if personInfo_name != 'Unknow':
                        if personInfo_name in self.Friend:
                            pass
                        else:
                            self.Friend.append(personInfo_name)
                            Update = True
                    index = index+1
                    check =True
                    if personInfo_name=='Unknow':
                        color = (0,0,255)
                        thickline = 3
                        check = False
                    if AutoCheck:
                        if personInfo_name in SearchNameList:
                            color = (0,215,255)
                    self.drawStyle(frame,left,top,right,bottom,left_right,top_bottom,color,thickline)
                    #co = '( %.2f,%.2f)'%((left+right)/2.0,(top+bottom)/2.0)
                    font_size = left_right//3
                    #cv2.putText(frame,co,(right,top-font_size),cv2.FONT_HERSHEY_SIMPLEX ,1,color,1)
                    frame = self.drawChineseText(frame,font_size,(left,top-font_size*1.2),personInfo_name+'    dist:'+str(round(personInfo_dist,2)),check)
                    if AutoCheck:
                        if AutoSound:
                            if personInfo_name in SearchNameList:
                                self.AutoSound(personInfo_name,1,0.01)
                        if AutoScreenShot:
                            if personInfo_name in SearchNameList:
                                localTime = time.localtime()
                                timeUnix = time.strftime('%Y-%m-%d_%H-%M-%S',localTime)
                                filename = DefaultSavePath+'img_'+timeUnix+'.jpg'
                                if cv2.imwrite(filename,frame):
                                    print('截图保存成功，路径为  :%s'%filename)
                                else:
                                    print('截图保存失败')
                        if AutoStop:
                            delay = 10
                            if personInfo_name in SearchNameList:
                                print('检测到 %s'%personInfo_name)
                                if delay >=0 and cv2.waitKey(delay):
                                    cv2.waitKey(0)

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
            self.num = self.num + 1
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
            if Update:
                if len(self.Friend)>0:
                    print('识别出的人脸:',self.Friend)
                    Update = False
            
        video_capture.release()
        cv2.destroyAllWindows()
        
    
if __name__=='__main__':
    '''
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
    self.face_box_draw_video(model)
    video_time2 = time.time()
    print('Friends:',self.Friend)
    print('drawStyle_cost平均时间：%.2fs'%np.mean(drawStyle_cost))
    print('drawChineseText平均时间：%.2fs'%np.mean(drawChineseText_cost))
    print('search_name_cost平均时间：%.2fs'%np.mean(search_name_cost))
    print('detect_face_cost平均时间：%.2fs'%np.mean(detect_face_cost))
    if self.num>0:
        print('face_box_draw_video平均时间：%.2fs'%(float((video_time2-video_time1))/(num*1.0)))
    print('程序结束...')
    '''
    face_draw_main().AutoSound('DD4')