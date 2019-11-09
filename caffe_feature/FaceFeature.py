#coding=utf-8
import sys
sys.path.insert(0, '/data/drivers/caffe/python')#caffe的python环境变量所在位置
import caffe
import cv2
import numpy as np
import random
import os
import pdb
import settings
from numpy import linalg as LA



# os.environ["CUDA_VISIBLE_DEVICES"] = "7"
#=====================================FACE ALIGNED=======================================================================
RefShape = [-27.606326, -30.763604,
            27.604702, -30.764311,
            0.002382, 1.479138,
            -23.444776, 30.02466,
            23.444018, 30.024117]

base_dir = os.path.dirname(os.path.abspath(__file__))#当前目录
deploy = os.path.join(base_dir,"model.prototxt")#caffe模型权重文件路径
weight = os.path.join(base_dir,"model.caffemodel")##caffe模型权重文件路径



class FaceFeature(object):
    def __init__(self):
        self.deploy = deploy
        self.weight = weight
        self.net = self.load_model(self.deploy, self.weight, is_cuda=False)
    def calcProcrustes(self,predict_shape, ref_shape ):
        rigid_transform = [0,0,0,0,0,0]
        X1 = 0
        Y1 = 0
        Z = 0
        C1 = 0
        C2 = 0

        for i in range(5):
            x1 = predict_shape[i*2]
            y1 = predict_shape[i*2+1]
            x2 = ref_shape[i*2]
            y2 = ref_shape[i*2+1]
            X1 += x1
            Y1 += y1
            Z += x2*x2 + y2*y2
            C1 += x1 * x2 + y1 * y2
            C2 += y1 * x2 - x1 * y2

        temp_a = C1 / Z
        temp_b = C2 / Z
        rigid_transform[0] = temp_a
        rigid_transform[1] = -temp_b
        rigid_transform[2] = temp_b
        rigid_transform[3] = temp_a
        rigid_transform[4] = X1 / 5
        rigid_transform[5] = Y1 / 5

        return rigid_transform

    def cropAlignedFaceImage(self,rigidTransform, initImg, width = 128, bilinear = True):
        RefShapeX = 58 + 6 + (width - 128)/2
        RefShapeY = 58.3698 + 6 + (width - 128)/2

        imgW = initImg.shape[1]
        imgH = initImg.shape[0]

        r00 = rigidTransform[0]
        r01 = rigidTransform[1]
        r10 = rigidTransform[2]
        r11 = rigidTransform[3]
        tx = rigidTransform[4]
        ty = rigidTransform[5]

        y, x = np.mgrid[0:width, 0:width]

        initX = r00*(x-RefShapeX) + r01*(y-RefShapeY) + tx
        initY = r10*(x-RefShapeX) + r11*(y-RefShapeY) + ty
        initX = np.clip(initX, 0, imgW-2)
        initY = np.clip(initY, 0, imgH-2)

        if bilinear:
            cropImg = self.bilinear_interpolate(initImg, initX, initY)
        else:
            cropImg = self.nearest_interpolate(initImg, initX, initY)
        return cropImg

    def bilinear_interpolate(self,im, x, y):
        x0 = np.floor(x).astype(int)
        y0 = np.floor(y).astype(int)
        x1 = x0 + 1
        y1 = y0 + 1

        Ia = im[ y0, x0 ]
        Ib = im[ y1, x0 ]
        Ic = im[ y0, x1 ]
        Id = im[ y1, x1 ]

        wa = (x1-x) * (y1-y)
        wb = (x1-x) * (y-y0)
        wc = (x-x0) * (y1-y)
        wd = (x-x0) * (y-y0)
        return wa*Ia + wb*Ib + wc*Ic + wd*Id

    def nearest_interpolate(self,im, x, y):
        x0 = np.floor(x+0.5).astype(int)
        y0 = np.floor(y+0.5).astype(int)
        Ia = im[ y0, x0 ]
        return Ia

    def AlignedFace_from_5points(self,points, gray, width = 128, bilinear = True):
        rigid_transform = self.calcProcrustes(points, RefShape)
        crop_img = self.cropAlignedFaceImage(rigid_transform, gray, width, bilinear = bilinear)
        return np.uint8(crop_img)

    def load_model(self,protofile, weightfile, is_cuda = False):
        if is_cuda:
            caffe.set_device(0)
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()
        net = caffe.Net(protofile, weightfile, caffe.TEST)
        return net

    def extract_feature(self,net,  image):
        net.blobs['data'].data[...] = image
        output = net.forward()
        np_features = np.array(output['fc6'])
        return np_features

    def get_feature(self,imgpath,points):
        '''
        提取特征向量
        :param imgpath: 图片路径
        :param points: 五官坐标
        :return: 图片对应的特征向量
        '''
        img = cv2.imread(imgpath, 0)
        aligned_img = self.AlignedFace_from_5points(points, img, width=128, bilinear=True)
        aligned_img = aligned_img.reshape([1,1,128,128])-128.0
        #net = self.load_model(deploy, weight, is_cuda=False)
        fea = self.extract_feature(self.net, aligned_img)
        return fea

    def ConsinDistance(self,feaV1, feaV2):
        '''
        计算余弦值
        :param feaV1: 特征向量
        :param feaV2: 特征向量
        :return: 余弦值
        '''
        feaV1 = feaV1.astype(np.float32).reshape([-1])
        feaV2 = feaV2.astype(np.float32).reshape([-1])
        
        return np.dot(feaV1, feaV2) / (LA.norm(feaV1) * LA.norm(feaV2))
        
        
if __name__ == '__main__':
    #调用示例
    path1 = "./1545097238_Face_0.jpg"
    path2 = "./1545103049_Face_0.jpg"
    pts1 = [125.003,103.713,167.117,108.393,156.588,138.808,122.664,164.544,154.249,166.883]
    pts2 = [147.073,98.3265,183.607,104.85,182.302,138.774,132.721,160.955,162.731,167.479]
    faceobj = FaceFeature()
    fea1 = faceobj.get_feature(path1,pts1)
    fea2 = faceobj.get_feature(path2,pts2)
    print faceobj.ConsinDistance(fea1, fea2)
