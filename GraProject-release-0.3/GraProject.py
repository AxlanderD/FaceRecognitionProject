from Ui_Graproject import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QSplashScreen,QMessageBox
from PyQt5.QtCore import QTimer,QCoreApplication,Qt,QObject,pyqtSignal
from PyQt5.QtGui import QPixmap,QTextCursor,QMovie
import qimage2ndarray
import cv2
import time
import face_draw_main_
from multiprocessing import Process
import face_comm
import json

class Show(QMainWindow,Ui_MainWindow,Process):
    def __init__(self,parent = None):
        super(Show,self).__init__(parent)
        self.setupUi(self)
        #self.loadingImgThread = threading.Thread(target = self.LoadingImg)
        #控制台信息输出重定向
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)
        self.parameters()
        self.CallBackFunc()
        #self.Timer = QTimer()
        #self.Timer.timeout.connect(self.TimeOutFunc)
        #保存功能先不做了把相关的元件隐藏
        self.SaveBt.setVisible(False)
        self.StopBt.setVisible(False)
        #初始化输出QLabel
        self.LoadOver = False
        self.MsgEdit.append('人脸识别前请加载检测识别模块...')
        #初始化自动控制
        self.AutoCheck = False
        self.AutoStop = False
        self.AutoScreenShot = False
        self.AutoSound = False
        self.SearchNameList = []
        #初始化参数 回调函数
        


        self.gif = QMovie("back_pic/back_gif.gif")
        self.ShowImgLabel.setMovie(self.gif)
        self.gif.start()


    #播放gif图
    def loadGif(self):
        self.gif = QMovie("back_pic/back_gif.gif")
        self.ShowImgLabel.setMovie(self.gif)
        self.gif.start()
    
    #点击自动控制开关
    def AutoControlOpen(self):
        if self.AutoCheckControlBt.isChecked():
            print('开启自动控制\n')
            self.AutoCheck = True
            self.groupBox.setVisible(True)
            self.label_4.setVisible(True)
            self.label_5.setVisible(True)
            self.savePathBt.setVisible(True)
            self.savePathEdit.setVisible(True)
            self.ConfirmSearchNameBt.setVisible(True)
            self.SearchNameEdit.setVisible(True)
        else:
            print('关闭自动控制\n')
            self.AutoCheck = False
            self.groupBox.setVisible(False)
            self.label_4.setVisible(False)
            self.label_5.setVisible(False)
            self.savePathBt.setVisible(False)
            self.savePathEdit.setVisible(False)
            self.ConfirmSearchNameBt.setVisible(False)
            self.SearchNameEdit.setVisible(False)

    def autoStopOpen(self):
        if self.autoStopBt.isChecked():
            print('开启自动停止\n')
            self.AutoStop = True
        else:
            print('关闭自动停止\n')
            self.AutoStop = False
    
    def autoGetPicOpen(self):
        if self.autoGetPicBt.isChecked():
            print('开启自动截图\n')
            self.AutoScreenShot = True
            self.savePathBt.setEnabled(True)
        else:
            print('关闭自动截图\n')
            self.AutoScreenShot = False
            self.savePathBt.setEnabled(False)
    
    def autoSoundOpen(self):
        if self.autoSoundBt.isChecked():
            print('开启自动语音提示\n')
            self.AutoSound = True
        else:
            print('关闭自动语音提示\n')
            self.AutoSound = False
    
    #获取搜索列表
    def getSearchName(self):
        if self.SearchNameEdit.text() == '':
            QMessageBox.information(self,'警告','    搜索目标为空    ')
        else:
            SearchNameList = self.SearchNameEdit.text()
            #对字符串进行处理，去掉空格,去除重复元素
            SearchNameList = set(SearchNameList.split())
            self.MsgEdit.append('想要搜索的目标列表：%s'%SearchNameList)
            json_path = face_comm.get_conf('json','json_path')
            with open(json_path,'r',encoding='UTF-8') as f:
                lines = f.read()
                lines = json.loads(lines)
            #判断输入的人名是否在数据库中
            #这里集合在循环中删除元素后会报错 RuntimeError: Set changed size during iteration
            SearchNameListCopy = SearchNameList.copy()
            for SearchName in SearchNameList:
                get = False
                for line in lines:
                    if line['name']  == SearchName:
                        get = True
                        break
                if get == False:
                    self.MsgEdit.append('%s 在数据库中没有记录,搜索时将被忽略'%SearchName)
                    QMessageBox.information(self,'无记录','搜索目标%s不存在于数据库中！'%SearchName)
                    SearchNameListCopy.discard(SearchName)
            if len(SearchNameList)>0:
                self.MsgEdit.append('选择的搜索目标名单：%s'%list(SearchNameListCopy))
                self.SearchNameList = list(SearchNameListCopy)
            else:
                self.MsgEdit.append('搜索名单为空')

    #加载模块
    def load_model(self):
        #self.loadingImgThread.setDaemon(True)
        #self.loadingImgThread.start()
        self.ShowImgLabel.clear()
        if self.LoadOver == False:
            self.LoadOver = True
            if self.LoadOver:
                self.StartBt.setEnabled(True)
                self.MsgEdit.append('模块加载中......\n')
                #P1 = Process(target=face_draw_main_.face_draw_main,name = 'LoadThread')
                #P1.daemon(True)
                #P1.start() 
                faceDraw = face_draw_main_.face_draw_main()
                self.MsgEdit.append('模块加载完毕！\n')
                #self.LoadOver = False
                self.face_draw_pic = faceDraw.face_box_draw
                self.face_draw_video = faceDraw.face_box_draw_video
                #self.gif.stop()
        else:
            print('模块已经加载完成！请勿重复加载')
        

    #参数管理
    def parameters(self):
        #自动控制开关 初始化不可见
        self.savePathBt.setEnabled(False)
        self.groupBox.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.savePathBt.setVisible(False)
        self.savePathEdit.setVisible(False)
        self.ConfirmSearchNameBt.setVisible(False)
        self.SearchNameEdit.setVisible(False)

        self.StartBt.setEnabled(False)
        self.MsgEdit.clear()
        self.ShowImgLabel.clear()
        self.DefaultOpenPath = 'pic/'
        self.DefaultSavePath = 'imgData/'
        self.UseLocalCamera = False
        self.StartFaceReg = False
        self.makeVideo = False
        self.OpenPath.setText(self.DefaultOpenPath)
        #self.SavePath.setText(self.DefaultSavePath)
        #self.pic_model.setChecked(True)
        self.IpPath.setVisible(False)
        self.StopBt.setDisabled(True)
        self.SaveBt.setDisabled(True)
        #输入Camera信息组件
        self.label_6.setVisible(False)
        self.IpPath.setVisible(False)
        self.UserName.setVisible(False)
        self.UserPwd.setVisible(False)
        self.ConfirmCameraBt.setVisible(False)
        self.LocalCamera.setVisible(False)
        #Label初始化
        self.ShowImgLabel.setScaledContents(True)
    #获取选择的模式
    def getSelectModel(self):
        sender = self.sender()
        self.SelectModel =  sender.text()
        self.MsgEdit.append('选择模式: %s '%self.SelectModel)
        if self.SelectModel == '视频':
            self.MsgEdit.append('-----Esc键关闭摄像头-----')
            self.MsgEdit.append('-----空格键对画面进行截图-----')
            self.ShowImgLabel.clear()
            self.IpPath.setVisible(False)
            self.StopBt.setDisabled(False)
            self.SaveBt.setDisabled(True)
            self.label_6.setVisible(False)
            self.IpPath.setVisible(False)
            self.UserName.setVisible(False)
            self.UserPwd.setVisible(False)
            self.ConfirmCameraBt.setVisible(False)
            self.LocalCamera.setVisible(False)
            self.ShowImg = cv2.VideoCapture(self.DefaultOpenPath)
        elif  self.SelectModel == '摄像头':
            self.MsgEdit.append('-----Esc键关闭摄像头-----')
            self.MsgEdit.append('-----空格键对画面进行截图-----')
            self.ShowImgLabel.clear()
            self.StopBt.setDisabled(False)
            self.SaveBt.setDisabled(False)
            self.IpPath.setVisible(True)
            self.label_6.setVisible(True)
            self.IpPath.setVisible(True)
            self.UserName.setVisible(True)
            self.UserPwd.setVisible(True)
            self.ConfirmCameraBt.setVisible(True)
            self.LocalCamera.setVisible(True)
            self.LocalCamera.setDisabled(False)
            self.SaveBt.setText('录像')
        elif self.SelectModel == '图片':
            self.ShowImgLabel.clear()
            self.IpPath.setVisible(False)
            self.StopBt.setDisabled(True)
            self.SaveBt.setDisabled(True)
            self.label_6.setVisible(False)
            self.IpPath.setVisible(False)
            self.UserName.setVisible(False)
            self.UserPwd.setVisible(False)
            self.ConfirmCameraBt.setVisible(False)
            self.LocalCamera.setVisible(False)
            self.SaveBt.setText('保存')
    #打开本地摄像头
    def OpenLocalCamera(self):
        if self.LocalCamera.isChecked():
            self.ConfirmCameraBt.setDisabled(True)
            self.UseLocalCamera = True
            self.CameraUserName =''
            self.CameraIP =''
            self.CameraUserPwd = ''
            self.IpPath.setText('')
            self.UserName.setText('')
            self.UserPwd.setText('')
        else:
            self.ConfirmCameraBt.setDisabled(False)
            self.UseLocalCamera = False

    #获取摄像头信息
    def getCameraInfo(self):
        self.LocalCamera.setDisabled(True)
        self.CameraIP = self.IpPath.text()
        self.CameraUserName = self.UserName.text()
        self.CameraUserPwd = self.UserPwd.text()
        self.MsgEdit.append('CameraIP:%s'%self.CameraIP)
        self.MsgEdit.append('CameraUserName:%s'%self.CameraUserName)
        self.MsgEdit.append('CameraUserPwd:******')

    #设置保存文件夹的路径
    def SetSavePath(self):
        dirname = QFileDialog.getExistingDirectory(self,'浏览文件夹','.')
        self.savePathEdit.setText(dirname)
        self.DefaultSavePath = dirname+'/'
        self.MsgEdit.append('保存路径设置: %s '%dirname)
            
    #设置打开文件的路径
    def SetOpenPath(self):
        try:
            filename = QFileDialog.getOpenFileName(self,'浏览文件','.')
            self.OpenPath.setText(str(filename[0]))
            self.DefaultOpenPath = filename[0]
            self.MsgEdit.append('打开文件 : %s '%filename[0])
        except Exception as e :
            self.MsgEdit.append(str(e))

    #开始运行按钮
    def StartShowImg(self):
        try:
            autoControl = [self.AutoCheck,self.AutoStop,self.AutoScreenShot,self.AutoSound,self.SearchNameList,self.DefaultSavePath]
            if self.SelectModel == '图片':
                '''
                    显示图片需要OpenCv先读入 返回图片矩阵后进行处理
                    OpenCv的颜色格式是bgr需要先转化为rgb格式
                    Label可以接受的图像类型为QPixmap 其颜色通道为RGB
                    因此需要先对颜色进行调整然后再调用array2qimage将其变为QImage格式
                '''
                self.ShowImg = cv2.imread(self.DefaultOpenPath)
                self.MsgEdit.append('打开的文件路径:%s'%self.DefaultOpenPath)
                if self.ShowImg is not None:
                    Img = cv2.cvtColor(self.ShowImg,cv2.COLOR_BGR2RGB)
                    Qimg = qimage2ndarray.array2qimage(Img)
                    self.ShowImgLabel.setPixmap(QPixmap(Qimg))
                    self.ShowImgLabel.show()
                    self.face_draw_pic(self.DefaultOpenPath,autoControl)
                else:
                    self.MsgEdit.append('Img Open failed...')
            elif self.SelectModel == '视频':
                
                #self.ShowImg = cv2.VideoCapture(self.DefaultOpenPath)
                self.face_draw_video('video',self.DefaultOpenPath,'','','',autoControl)
                #self.Timer.start(200)
            elif self.SelectModel == '摄像头':
                if self.UseLocalCamera==False:
                    #self.ShowImg = cv2.VideoCapture('http://%s:%s:%s:8081'%(self.CameraUserName,self.CameraUserPwd,self.CameraIP))
                    self.MsgEdit.append('打开指定IP摄像头...IP: %s '%self.CameraIP)
                    #self.Timer.start(1)
                    self.face_draw_video('camera',self.DefaultOpenPath,self.CameraUserName,self.CameraUserPwd,self.CameraIP,autoControl)
                    
                elif self.UseLocalCamera ==True :
                    #self.ShowImg = cv2.VideoCapture(0)
                    self.MsgEdit.append('打开默认摄像头...')
                    #self.Timer.start(200)
                    self.face_draw_video('camera','','','','',autoControl)
                    
        except Exception as e:
            self.MsgEdit.append(str(e))
    '''
    def TimeOutFunc(self):
        while self.LoadOver:
            suc,Img =self.loadingImg.read()
            if suc:
                Img = cv2.cvtColor(Img,cv2.COLOR_BGR2RGB)
                Qimg = qimage2ndarray.array2qimage(Img)
                self.ShowImgLabel.setPixmap(QPixmap(Qimg))
                self.ShowImgLabel.show()   
            else:
                self.MsgEdit.append('Image obtaining failed.')
'''
    #暂停按钮的设置
    def StopCamera(self):
        if self.StopBt.text() == '暂停' and self.SelectModel == '摄像头' and self.makeVideo == False:
            self.StopBt.setText('继续')
            self.MsgEdit.append('暂停播放...')
            self.SaveBt.setText('保存')
            self.Timer.stop()
        elif self.StopBt.text() == '继续' and self.SelectModel == '摄像头' and self.makeVideo == False:
            self.StopBt.setText('暂停')
            self.MsgEdit.append('继续播放...')
            self.SaveBt.setText('录像')
            self.Timer.start(1)
        elif self.StopBt.text() == '暂停' and self.SelectModel == '摄像头' and self.makeVideo == True:
            self.StopBt.setText('继续')
            self.MsgEdit.append('暂停播放...')
            self.Timer.stop()
        elif self.StopBt.text() == '继续' and self.SelectModel == '摄像头' and self.makeVideo == True:
            self.StopBt.setText('暂停')
            self.MsgEdit.append('继续播放...')
            self.Timer.start(1)
        elif self.StopBt.text() == '暂停' and self.SelectModel == '视频':
            self.StopBt.setText('继续')
            self.MsgEdit.append('暂停播放...')
            self.Timer.stop()
        elif self.StopBt.text() == '继续' and self.SelectModel == '视频':
            self.StopBt.setText('暂停')
            self.MsgEdit.append('继续播放...')
            self.Timer.stop(1)
        
    #选择了录像
    def SaveVideo(self):
        if self.SaveBt.text() == '录像' and self.SelectModel == '摄像头' and self.makeVideo == False:
            self.SaveBt.setText('终止保存')
            self.makeVideo = True
            self.video_name = self.DefaultSavePath+'video'+time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))+'.avi'
            self.size = (self.ShowImg.shape[1],self.Image.shape[0])
        elif self.SaveBt.text() == '终止保存' and self.SelectModel == '摄像头' and self.makeVideo == True:
            self.SaveBt.setText('录像')
            self.makeVideo = False
            self.MsgEdit.append('视频保存于 %s'%self.DefaultSavePath)
        
    def Exit(self):
        self.close()

    def TimeOutFunc(self):
        while self.LoadOver:
            suc,Img =self.loadingImg.read()
            if suc:
                Img = cv2.cvtColor(Img,cv2.COLOR_BGR2RGB)
                Qimg = qimage2ndarray.array2qimage(Img)
                self.ShowImgLabel.setPixmap(QPixmap(Qimg))
                self.ShowImgLabel.show()   
            else:
                self.MsgEdit.append('Image obtaining failed.')

    #回调函数 当按键被点击时触发
    def CallBackFunc(self):
        self.AutoCheckControlBt.clicked.connect(self.AutoControlOpen)
        self.autoStopBt.clicked.connect(self.autoStopOpen)
        self.autoGetPicBt.clicked.connect(self.autoGetPicOpen)
        self.autoSoundBt.clicked.connect(self.autoSoundOpen)
        self.savePathBt.clicked.connect(self.SetSavePath)
        self.ConfirmSearchNameBt.clicked.connect(self.getSearchName)

        self.LoadMsg.clicked.connect(self.load_model)
        #self.SearchConfirmBt.clicked.connect(self.SetSavePath)
        self.OpenPathBt.clicked.connect(self.SetOpenPath)
        '''
            将这三个radioButton和一个槽函数绑定
            槽函数就是这三个对象，其中任意的一个对象的操作所发出的信号都会使得其他对象能够接收到信号
            即通过动作触发特定函数
        '''
        self.pic_model.clicked.connect(self.getSelectModel)
        self.video_model.clicked.connect(self.getSelectModel)
        self.camera_model.clicked.connect(self.getSelectModel)
        self.ConfirmCameraBt.clicked.connect(self.getCameraInfo)
        self.StartBt.clicked.connect(self.StartShowImg)
        self.StopBt.clicked.connect(self.StopCamera)
        self.SaveBt.clicked.connect(self.SaveVideo)
        self.LocalCamera.clicked.connect(self.OpenLocalCamera)
        self.ExitBt.clicked.connect(self.Exit)
        #每隔一段时间调用一次
        #self.Timer.timeout.connect(self.TimerOutFun)

    def outputWritten(self, text):
        cursor = self.MsgEdit.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.MsgEdit.setTextCursor(cursor)
        self.MsgEdit.ensureCursorVisible()

        
class EmittingStream(QObject):  
        textWritten = pyqtSignal(str)  #定义一个发送str的信号
        def write(self, text):
            self.textWritten.emit(str(text))           

        
if __name__=='__main__':
    app = QApplication(sys.argv)
    splash = QSplashScreen(QPixmap("back_pic/loadMain.jpg"))
    splash.show()
    time.sleep(5)
    ui = Show()
    ui.show()
    splash.finish(ui)
    sys.exit(app.exec_())