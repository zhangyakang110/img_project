# -*- coding:utf-8 -*-
import os
import sys
import numpy as np
import cv2
from scipy import misc
import tensorflow as tf
import pdb
from mtcnn_code import detect_face

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
REPO_DIRNAME = os.path.dirname(os.path.abspath(__file__))

default_args = {
    'mtcnn_model_dir': (
        '{}/'.format(REPO_DIRNAME)),
    }
default_args['gpu_memory_fraction'] = 0.25
default_args['margin'] = 10#32
default_args['minsize'] = 20 #minimum size of face
default_args['threshold'] = [0.6, 0.7, 0.7]  # three steps's threshold
default_args['factor'] = 0.709#0.709  # scale factor

class FaceAlignmentor(object):

    def __init__(self, mtcnn_model_dir, gpu_memory_fraction,
                 margin, minsize, threshold, factor):

        with tf.Graph().as_default():
            gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=gpu_memory_fraction)
            sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
            with sess.as_default():
                self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(sess, mtcnn_model_dir)
        self.margin = margin
        self.minsize = minsize
        self.threshold = threshold
        self.factor = factor

    def get_aligned_faces(self, image,image_size=160):
        height,width,channel = image.shape
        scale = float(640)/width
        des_h = int(height*scale)
        tinyimage = cv2.resize(image,(640,des_h))
        bounding_boxes,points = detect_face.detect_face(tinyimage, self.minsize,self.pnet, self.rnet,
                                                    self.onet, self.threshold, self.factor)
        nrof_faces = bounding_boxes.shape[0]
        scaled_faces = []
        bbx = []
        if nrof_faces > 0:
            for face_position in bounding_boxes:
                det = face_position[0:4]
                img_size = np.asarray(image.shape)[0:2]
                bb = np.zeros(4, dtype=np.int32)
                bb[0] = int(np.maximum(det[0] - self.margin / 2, 0)/scale)
                bb[1] = int(np.maximum(det[1] - self.margin / 2, 0)/scale)
                bb[2] = int(np.minimum(det[2] + self.margin / 2, img_size[1])/scale)
                bb[3] = int(np.minimum(det[3] + self.margin / 2, img_size[0])/scale)
                cropped = image[bb[1]:bb[3], bb[0]:bb[2], :]
                scaled = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
                scaled_faces.append(scaled)
                face_position = face_position.astype(int)
                bbx.append(bb)
        return scaled_faces,np.array(points/scale),np.array(bbx)

fa = FaceAlignmentor(**default_args)

def detect_verify_extract(imagepath):
    result = {}
    try:
        image = cv2.imread(imagepath)
        #image of RGB
        scaled_faces,points,bounding_boxes = fa.get_aligned_faces(image)
        id = 1
        faces = []
        return points
    except Exception as e:
        errorMessage = '{}: {}'.format(imagepath, e)
        print(errorMessage)
    else:
        if image.ndim < 2:
            print('Unable to align "%s"' % imagepath)
        elif image.ndim == 2:
            image = facenet.to_rgb(image)
        image = image[:, :, 0:3]

def get_Key_Points(imgpath):
    key_p = []
    try:
        pts = detect_verify_extract(imgpath)
        print pts,type(pts)
        for n in range(5):
            key_p.append(int(pts[0+n,0]))
            key_p.append(int(pts[5+n,0]))
        print key_p
        return key_p
    except:
        return

if __name__ == '__main__':
    pdb.set_trace()
    imgpath = "/home/zhangyk/workspace/data/img/Face_Camera_OUT_02/1520-1566624342_Face_0.jpg"
    # imgpath = "./175-1566608420_Face_0.jpg"
    # imgpath = "./058a7.JPG"
    point_lst = get_Key_Points(imgpath)
