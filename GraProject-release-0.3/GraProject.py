from Ui_Graproject import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QSplashScreen
from PyQt5.QtCore import QTimer,QCoreApplication,Qt,QObject,pyqtSignal
from PyQt5.QtGui import QPixmap,QTextCursor,QMovie
import qimage2ndarray
import cv2
import time
import face_draw_main_
class Show(QMainWindow,Ui_MainWindow):
    def __init__(self,parent = None):
        super(Show,self).__init__(parent)
        self.setupUi(self)
        #self.loadingImgThread = threading.Thread(target = self.LoadingImg)
        sys.stdout = EmittingStream(textWritten=self.outputWritten)
        sys.stderr = EmittingStream(textWritten=self.outputWritten)
        
        self.parameters()
        self.CallBackFunc()
        self.MsgEdit.append('人脸识别前请加载检测识别模块...')
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.TimeOutFunc)
        #保存功能先不做了把相关的元件隐藏
        self.SaveBt.setVisible(False)
        self.label_4.setVisible(False)
        self.label_5.setVisible(False)
        self.SavePath.setVisible(False)
        self.SavePathBt.setVisible(False)
        self.StopBt.setVisible(False)
        self.LoadOver = False
        self.gif = QMovie("back_pic/back_gif.gif")

    #加载模块
    def load_model(self):
        #self.loadingImgThread.setDaemon(True)
        #self.loadingImgThread.start()
        self.ShowImgLabel.clear()
        if self.LoadOver == False:
            
            #self.ShowImgLabel.setMovie(self.gif)
            self.LoadOver = True
            if self.LoadOver:
                self.MsgEdit.append('模块加载中......\n')
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
        self.MsgEdit.clear()
        self.ShowImgLabel.clear()
        self.DefaultOpenPath = 'pic/'
        self.DefaultSavePath = 'SaveData/'
        self.UseLocalCamera = False
        self.StartFaceReg = False
        self.makeVideo = False
        self.OpenPath.setText(self.DefaultOpenPath)
        self.SavePath.setText(self.DefaultSavePath)
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
        self.SavePath.setText(dirname)
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
                    self.face_draw_pic(self.DefaultOpenPath)
                else:
                    self.MsgEdit.append('Img Open failed...')
            elif self.SelectModel == '视频':
                
                #self.ShowImg = cv2.VideoCapture(self.DefaultOpenPath)
                self.face_draw_video('video',self.DefaultOpenPath,'','','')
                #self.Timer.start(200)
            elif self.SelectModel == '摄像头':
                if self.UseLocalCamera==False:
                    #self.ShowImg = cv2.VideoCapture('http://%s:%s:%s:8081'%(self.CameraUserName,self.CameraUserPwd,self.CameraIP))
                    self.MsgEdit.append('打开指定IP摄像头...IP: %s '%self.CameraIP)
                    #self.Timer.start(1)
                    self.face_draw_video('camera',self.DefaultOpenPath,self.CameraUserName,self.CameraUserPwd,self.CameraIP)
                    
                elif self.UseLocalCamera ==True :
                    #self.ShowImg = cv2.VideoCapture(0)
                    self.MsgEdit.append('打开默认摄像头...')
                    #self.Timer.start(200)
                    self.face_draw_video('camera','','','','')
                    
        except Exception as e:
            self.MsgEdit.append(str(e))
    '''
    def LoadingImg(self):
        loadingImgPath = 'back_pic/back_gif.gif'
        self.loadingImg = cv2.VideoCapture(loadingImgPath)
        #self.Timer.start(1)
        self.TimeOutFunc()

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
        #self.Timer.Stop()
        #self.ShowImg.release()
        self.close()

    def LoadingImg(self):
        loadingImgPath = 'back_pic/back_gif.gif'
        self.loadingImg = cv2.VideoCapture(loadingImgPath)
        #self.Timer.start(1)
        self.TimeOutFunc()

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
        self.LoadMsg.clicked.connect(self.load_model)
        self.SavePathBt.clicked.connect(self.SetSavePath)
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