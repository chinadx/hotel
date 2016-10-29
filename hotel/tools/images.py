# -*- coding:utf-8 -*-
__author__ = 'Shaun'

import argparse
import cPickle
import logging
import numpy
import os.path
import PIL.Image
import sys
import glob
import cv2
import gzip
numpy.random.seed(51244)
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import SGD

def to_range(ary):  #change to +-1.0
    return ary* 2.0/255.0 - 1.0

def from_range(ary): #rechange from +-1.0
    return (ary + 1.0) * 255.0/2.0

def x_from_image(source, neighbors):  #get the x_train data
    img = PIL.Image.open(source)
    ary = to_range(numpy.array(img))
    enlarged_img = enlarged(ary, neighbors)      #边框填充
    patches = patchify(enlarged_img, neighbors)  #宽度为2*neighbors+1的n个矩阵
    return numpy.array(patches), ary.shape       #x_train data(每个像素点周围的(2n+1)平方像素点) ,原图shape


def y_from_image(source, neighbors): #get the y_train data
    output = []
    cleaned_path = os.path.join('./train_cleaned',os.path.basename(source))
    img = PIL.Image.open(cleaned_path)
    ary = to_range(numpy.array(img))
    height, width = ary.shape
    for i in xrange(height):
        for j in xrange(width):
            output.append(ary[i, j].flatten())  #flatten()??
    return output

def patchify(enlarged, neighbors):  #获取周围点组成集合
    output = []
    height, width = enlarged.shape
    for i in xrange(neighbors, height-neighbors):
        for j in xrange(neighbors, width-neighbors):
            patch = enlarged[i-neighbors:i+neighbors+1, j-neighbors:j+neighbors+1]
            output.append(patch.flatten())
    return output

def enlarged(ary, neighbors):  #填充外围边角
    height, width = ary.shape
    enlarged = numpy.zeros((height + 2 * neighbors, width + 2 * neighbors))
    # Fill in the corners
    enlarged[:neighbors,:neighbors] = ary[0, 0]
    enlarged[:neighbors,-neighbors:] = ary[0, -1]
    enlarged[-neighbors:,:neighbors] = ary[-1, 0]
    enlarged[-neighbors:,-neighbors:] = ary[-1, -1]
    # Fill in the edges
    enlarged[:neighbors, neighbors:-neighbors] = ary[0, :] # top
    enlarged[neighbors:-neighbors, :neighbors] = ary[:, 0][numpy.newaxis].T # left
    enlarged[-neighbors:, neighbors:-neighbors] = ary[-1, :] # top
    enlarged[neighbors:-neighbors, -neighbors:] = ary[:, -1][numpy.newaxis].T # right
    # Fill in the chewy center
    enlarged[neighbors:-neighbors,neighbors:-neighbors] = ary
    return enlarged

def load_training(limit=10,neighbors=2): #读取测试图片
    xs = []
    ys = []
    for path in glob.glob('./train/*.png')[:limit]:
        print '---------', path
        patches, _ = x_from_image(path, neighbors)
        solutions = y_from_image(path, neighbors)
        xs.extend(patches)
        ys.extend(solutions)
    return xs, ys

def save_training_data(x,y):  #保存测试图片
    f = open('training_data.pkl','wb')
    cPickle.dump(x,f,-1)
    cPickle.dump(y,f,-1)
    f.close()

def load_training_data():  #读取测试图片
    f = open('training_data.pkl')
    x = cPickle.load(f)
    y = cPickle.load(f)
    f.close()
    return x,y

def split_training(xs, ys):  #分出一部分测试集
    joined = zip(xs, ys)
    numpy.random.shuffle(joined)
    xs = [x for x, _ in joined]
    ys = [y for _, y in joined]
    train_count = int(len(xs)*9/10.0)
    valid_count = int(len(xs)/10.0)
    res = (xs[:train_count], ys[:train_count],xs[train_count:], ys[train_count:])
    return [numpy.array(r) for r in res]


'''
def build_model(input_size): #建模
    model = Sequential()
    model.add(Dense(input_size, 512, init='lecun_uniform'))
    model.add(Activation('tanh'))                             #激活函数不能随意选择，这里处理的数据是+-1.0 用tanh做激活函数？
    model.add(Dense(512, 256, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dense(256, 128, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dense(128, 64, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dense(64, 1, init='lecun_uniform'))
    model.add(Activation('tanh'))
    sgd = SGD(lr=0.01, momentum=0.9) # , nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)
    return model
'''

def build_model(input_size): #建模
    model = Sequential()
    model.add(Dense(input_size, 512, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.25))
    model.add(Dense(512, 512, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.25))
    model.add(Dense(512, 256, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.25))
    model.add(Dense(256, 128, init='lecun_uniform'))
    model.add(Activation('tanh'))
    model.add(Dropout(0.5))
    model.add(Dense(128, 1, init='lecun_uniform'))
    model.add(Activation('tanh'))
    sgd = SGD(lr=0.05, momentum=0.9) # , nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd)
    return model

def train(limit=10, neighbors=2, epochs=10, batch_size=500):  #训练
    print 'loading data...'
    if os.path.exists('./training_data.pkl'):
        xs,ys = load_training_data()
    else:
        xs,ys = load_training(limit, neighbors)
        save_training_data(xs,ys)
        print 'the training_data has been saved!'
    print xs, '------------', ys
    train_x, train_y, valid_x, valid_y= split_training(xs, ys)
    print 'building model...'
    print train_x, train_y, valid_x, valid_y
    model = build_model(len(train_x[0]))
    if os.path.exists('./clean_weight'):
        model.load_weights(filepath = 'clean_weight')
    model.fit(train_x, train_y,
              nb_epoch=epochs,
              batch_size=batch_size,
              show_accuracy=True,
              validation_data=(valid_x, valid_y))
    model.save_weights(filepath='clean_weight',overwrite=True)


def load_test_images(limit=None, neighbors=2):  #读取测试图片
    image_specs = []
    xs = []
    for path in glob.glob('./test/*.png')[:limit]:
        image_number = os.path.basename(path)[:-len('.png')]
        patches, shape = x_from_image(path, neighbors)
        image_specs.append((image_number, shape))  #图片代号，形状
        xs.append(patches) #数据
    return image_specs, xs  #(代号，形状),训练数据

def create_pictures(limit=5):  #生成新的clean图片
    imgs = []
    image_specs, xs = load_test_images(limit=limit) #(代号，形状),训练数据
    model = build_model(25)   #if neighbors ==2   (2*n+1)^2
    model.load_weights(filepath = 'clean_weight')
    for (num, shape), patches in zip(image_specs, xs):
        predictions = model.predict(patches)
        shaped = from_range(predictions.reshape(shape))  #还原
        img = PIL.Image.fromarray(shaped)
        add = './clean/'+str(num)+'.Bmp'
        imgs.append(img)
        img = numpy.array(img)
        cv2.imwrite(add,img)        #保存图片
    return image_specs, imgs #(代号，形状),图片



if __name__ == '__main__':
    train(limit=10, neighbors=2, epochs=35, batch_size=10)
    # image_specs,imgs = create_pictures(limit = None)
