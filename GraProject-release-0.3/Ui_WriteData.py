# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Program File\Jupyter-NoteBook\Graduation Project\GraProject-release-0.3\WriteData.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_WriteFaces(object):
    def setupUi(self, WriteFaces):
        WriteFaces.setObjectName("WriteFaces")
        WriteFaces.resize(800, 600)
        WriteFaces.setMinimumSize(QtCore.QSize(800, 600))
        WriteFaces.setMaximumSize(QtCore.QSize(800, 600))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/人脸识别系统.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        WriteFaces.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(WriteFaces)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 0, 600, 400))
        font = QtGui.QFont()
        font.setFamily("楷体")
        self.frame.setFont(font)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame.setObjectName("frame")
        self.ImgLabel = QtWidgets.QLabel(self.frame)
        self.ImgLabel.setGeometry(QtCore.QRect(10, 10, 580, 380))
        self.ImgLabel.setText("")
        self.ImgLabel.setObjectName("ImgLabel")
        self.LoadImgPath = QtWidgets.QLineEdit(self.centralwidget)
        self.LoadImgPath.setGeometry(QtCore.QRect(10, 410, 420, 25))
        self.LoadImgPath.setReadOnly(True)
        self.LoadImgPath.setObjectName("LoadImgPath")
        self.ImgSavePath = QtWidgets.QLineEdit(self.centralwidget)
        self.ImgSavePath.setGeometry(QtCore.QRect(10, 450, 420, 25))
        self.ImgSavePath.setReadOnly(True)
        self.ImgSavePath.setObjectName("ImgSavePath")
        self.LoadPathBt = QtWidgets.QPushButton(self.centralwidget)
        self.LoadPathBt.setGeometry(QtCore.QRect(510, 410, 100, 25))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/打开文件.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.LoadPathBt.setIcon(icon1)
        self.LoadPathBt.setObjectName("LoadPathBt")
        self.SavePathBt = QtWidgets.QPushButton(self.centralwidget)
        self.SavePathBt.setGeometry(QtCore.QRect(510, 450, 100, 25))
        self.SavePathBt.setIcon(icon1)
        self.SavePathBt.setObjectName("SavePathBt")
        self.IntoDatabaseBt = QtWidgets.QPushButton(self.centralwidget)
        self.IntoDatabaseBt.setGeometry(QtCore.QRect(510, 510, 100, 25))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/确认.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.IntoDatabaseBt.setIcon(icon2)
        self.IntoDatabaseBt.setObjectName("IntoDatabaseBt")
        self.InputName = QtWidgets.QLineEdit(self.centralwidget)
        self.InputName.setGeometry(QtCore.QRect(230, 510, 200, 25))
        self.InputName.setText("")
        self.InputName.setReadOnly(False)
        self.InputName.setObjectName("InputName")
        self.SaveFaceBt = QtWidgets.QPushButton(self.centralwidget)
        self.SaveFaceBt.setGeometry(QtCore.QRect(630, 100, 150, 40))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icon/保存.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveFaceBt.setIcon(icon3)
        self.SaveFaceBt.setObjectName("SaveFaceBt")
        self.UnSaveBt = QtWidgets.QPushButton(self.centralwidget)
        self.UnSaveBt.setGeometry(QtCore.QRect(630, 170, 150, 40))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icon/不保存项目.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.UnSaveBt.setIcon(icon4)
        self.UnSaveBt.setObjectName("UnSaveBt")
        self.AlignFace = QtWidgets.QPushButton(self.centralwidget)
        self.AlignFace.setGeometry(QtCore.QRect(630, 30, 150, 40))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icon/人脸识别.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AlignFace.setIcon(icon5)
        self.AlignFace.setObjectName("AlignFace")
        self.InputID = QtWidgets.QLineEdit(self.centralwidget)
        self.InputID.setGeometry(QtCore.QRect(10, 510, 200, 25))
        self.InputID.setObjectName("InputID")
        self.showDataEt = QtWidgets.QTextEdit(self.centralwidget)
        self.showDataEt.setGeometry(QtCore.QRect(630, 240, 151, 291))
        self.showDataEt.setStyleSheet("#showDataEt{\n"
"    background-color:black;\n"
"    color:white;\n"
"}")
        self.showDataEt.setReadOnly(True)
        self.showDataEt.setObjectName("showDataEt")
        WriteFaces.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WriteFaces)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        WriteFaces.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WriteFaces)
        self.statusbar.setObjectName("statusbar")
        WriteFaces.setStatusBar(self.statusbar)

        self.retranslateUi(WriteFaces)
        QtCore.QMetaObject.connectSlotsByName(WriteFaces)

    def retranslateUi(self, WriteFaces):
        _translate = QtCore.QCoreApplication.translate
        WriteFaces.setWindowTitle(_translate("WriteFaces", "Write faces to database"))
        self.LoadImgPath.setPlaceholderText(_translate("WriteFaces", "数据载入路径"))
        self.ImgSavePath.setPlaceholderText(_translate("WriteFaces", "文件保存路径 默认alignface/"))
        self.LoadPathBt.setText(_translate("WriteFaces", "确认路径"))
        self.SavePathBt.setText(_translate("WriteFaces", "确认路径"))
        self.IntoDatabaseBt.setText(_translate("WriteFaces", "录入数据库"))
        self.InputName.setPlaceholderText(_translate("WriteFaces", "请输入姓名"))
        self.SaveFaceBt.setText(_translate("WriteFaces", "确认保存该人脸"))
        self.UnSaveBt.setText(_translate("WriteFaces", "不保存该人脸"))
        self.AlignFace.setText(_translate("WriteFaces", "获得对齐人脸"))
        self.InputID.setPlaceholderText(_translate("WriteFaces", "请输入ID"))
        self.showDataEt.setHtml(_translate("WriteFaces", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))

