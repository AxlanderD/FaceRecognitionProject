from Ui_WriteData import Ui_WriteFaces
import sys
import os
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QSplashScreen,QMessageBox
from PyQt5.QtCore import QTimer,QCoreApplication,Qt,QObject,pyqtSignal
from PyQt5.QtGui import QPixmap,QTextCursor,QMovie
import qimage2ndarray
import cv2
import time
import face_comm
import face_alignment
import face_annoy
import json
import face_detect
import random
import time

class GetFaces(QMainWindow,Ui_WriteFaces):
    def __init__(self,parent = None):
        super(GetFaces,self).__init__(parent)
        self.setupUi(self)
        self.parameters()
        self.CallBackFunc()
        self.annoy = face_annoy.face_annoy()
        self.detect = face_detect.Detect()

    def parameters(self):
        self.ImgLabel.clear()
        self.IntoDatabaseBt.setDisabled(True)
        self.SaveFaceBt.setDisabled(True)
        self.UnSaveBt.setDisabled(True)
        self.AlignFace.setDisabled(True)
        self.jsonPath = face_comm.get_conf("json","json_path")
        self.showDataEt.append("Show Exist Data:")
        with open(self.jsonPath,'r',encoding='UTF-8') as f:
            lines = f.read()
            lines = json.loads(lines)
        for line in lines:
            self.showDataEt.append("ID:"+line["id"]+" Name:"+line["name"])
        self.loadPath = ""
        self.savePath = "alignface/"

    def SetOpenPath(self):
        try:
            filename = QFileDialog.getOpenFileName(self,'浏览文件','.')
            self.LoadImgPath.setText(str(filename[0]))
            self.loadPath = filename[0]
            self.AlignFace.setDisabled(False)
        except Exception as e :
            self.showDataEt.append(str(e))

    def SetSavePath(self):
        dirname = QFileDialog.getExistingDirectory(self,'浏览文件夹','.')
        self.ImgSavePath.setText(dirname)
        self.savePath = dirname+'/'
        self.showDataEt.append('保存路径设置: %s '%dirname)

    def GetAlignFace(self):
        self.SaveFaceBt.setDisabled(False)
        self.UnSaveBt.setDisabled(False)
        self.AlignFace.setDisabled(False)
        self.ImgLabel.clear()
        result = self.detect.detect_face(self.loadPath)
        
        if len(result)>0:
            pic_array = cv2.imread(self.loadPath)
            align_face_array_list = face_alignment.align_face(pic_array,result['face_key_point'])
            for align_face_array in align_face_array_list:
                Img = cv2.cvtColor(align_face_array,cv2.COLOR_BGR2RGB)
                Qimg = qimage2ndarray.array2qimage(Img)
                self.Img_array = align_face_array
                self.ImgLabel.setPixmap(QPixmap(Qimg))
                self.ImgLabel.setScaledContents (True)
                self.ImgLabel.show()
        else:
            self.showDataEt.append("未发现人脸")
    
    def SaveAlignFace(self):
        self.IntoDatabaseBt.setDisabled(False)
        img = self.Img_array
        new_image_save_path= self.savePath+'%d_%d.png'%(time.time(),random.randint(0,100))
        self.save_align_face = new_image_save_path
        if cv2.imwrite(new_image_save_path,img):
            self.showDataEt.append('write success')       
        else:
            self.showDataEt.append('write failed')

    def UnSaveAlignFace(self):
        self.Img_array = ""
        self.ImgLabel.clear()

    def IntoDataBase(self):
        self.ID = self.InputID.text()
        self.Name = self.InputName.text()
        self.annoy.add_id_vector(self.loadPath,self.ID,self.Name)
        self.showDataEt.append("录入来源路径："+self.save_align_face)
        self.showDataEt.append("录入ID："+self.ID)
        self.showDataEt.append("录入Name："+self.Name)

    def CallBackFunc(self):
        self.LoadPathBt.clicked.connect(self.SetOpenPath)
        self.SavePathBt.clicked.connect(self.SetSavePath)
        self.AlignFace.clicked.connect(self.GetAlignFace)
        self.SaveFaceBt.clicked.connect(self.SaveAlignFace)
        self.UnSaveBt.clicked.connect(self.UnSaveAlignFace)
        self.IntoDatabaseBt.clicked.connect(self.IntoDataBase)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ui = GetFaces()
    ui.show()
    sys.exit(app.exec_())