这个文件中的model文件可以在github上找到，facenet和mtcnn的预训练模型。<br>
本次项目的具体流程<br>
<br>
<strong>主流程：</strong><br>
主程序入口文件为face_draw_main_.py<br>
0.初始化MTCNN和faceNet网络<br>
1.OpenCV打开摄像头或视频或图片<br>
2.MTCNN模型对图片数据进行人脸检测 （如果是视频的话，为了流畅性，可以每隔几帧进行一次检测）<br>
3.将检测到的结果通过OpenCV的仿射变换进行人脸对齐<br>
4.将对齐后的人脸传入faceNet进行特征提取以及人脸特征编码<br>
5.通过annoy索引在数据库中找到相似向量，通过欧式距离判别是否为同一个人<br>
6.返回得到的id并且绘制标注框和姓名<br>
<br>
<strong>人脸数据输入流程：</strong><br>
1.face_alignment.py模块中可以保存对齐后的人脸图片<br>
2.face_annoy.py模块将对齐后的人脸图片编码入库<br>
<br>
<strong>项目运行环境：</strong><br>
windows 10<br>
python 3.6<br>
mxnet-cu90 1.4.0<br>
tensorflow 1.5.0<br>
<br>
<strong>Ps:</strong>这里的tensorflow没有使用gpu版本，主要是因为使用的电脑显卡是GTX970m 显存3G，两个网络一起使用的时候会发生cudamalloc fail：out of memory 的问题。<br>
但是单个网络运行的时候都没有问题。<br>
目前想到的解决办法：<br>
1.有条件的话通过指定gpu，让两个网络运行在两个gpu上<br>
2.不使用mxnet版本的MTCNN，而是直接使用tensorflow版本的MTCNN（这里的MTCNN我有两个版本的，但是mxnet版本对于人脸的检测率更高一些..难以取舍:-）<br>
3.将faceNet或者MTCNN二者其一设置运行在cpu上<br>
目前我选择的是让faceNet使用cpu版本tensorflow..<br>
<br>
目前就先是这些。后续还会有更新..
<br>
==================05.04==================<br>
使用 PyQt5 添加了GUI界面<br>
<br>
入口程序改为GraProject.py<br>
==================05.06==================<br>
增加了检索目标自动语音提示,截图,视频停止功能<br>
修改了界面布局<br>
