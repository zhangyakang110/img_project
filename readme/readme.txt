环境配置
1. 环境列表：
/whls/requirements.txt
2. 安装环境：
cd 到whls目录下执行命令  pip install -r requirements.txt

模块说明：
1. caffe提取图片特征
	程序入口 /Img_project/caffe_feature/FaceFeature.py
2. face++人脸聚类，获取id
	程序入口/home/zhangyk/PycharmProjects/Img_project/Cluster_ID/GetID.py
3. Filter人脸选优
	程序入口/home/zhangyk/PycharmProjects/Img_project/Filter/filter.py
4. mtcnn人脸五官坐标检测
	程序入口/home/zhangyk/PycharmProjects/Img_project/mtcnn_code/Points.py
5. map系统调用
	程序入口/home/zhangyk/PycharmProjects/Img_project/post_rst/map_post.py
6. 共用模块
	xxxxx
7. redis路径切分
	程序入口/home/zhangyk/PycharmProjects/Img_project/RedisSplit/redis_handle.py
8. Dlib 人脸五官坐标检测
	程序入口/home/zhangyk/PycharmProjects/Img_project/Dlib_test/five_points.py



3.Dlib 配置
使用dlib库检测人脸五官坐标

1.相关环境配置
安装cmake
$ sudo apt-get install software-properties-common
$ sudo add-apt-repository ppa:george-edison55/cmake-3.x
$ sudo apt-get update
#如果之前没有装CMake，执行
$ sudo apt-get install cmake
#如果之前已经装过CMake
$ sudo apt-get upgrade
#再次查看cmake的版本:
$ cmake --version

2.dlib下载
https://github.com/davisking/dlib

$ mkdir Dlib
$ git init
$ git clone #复制clone地址

3.安装dlib
cd dlib
python setup.py install

4.安装scikit_image （图片处理可以使用opencv，或者 PIL）
pip install scikit_image

5.下载人脸关键点家测器

http://dlib.net/files/
