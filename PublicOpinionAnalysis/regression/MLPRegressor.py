#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# # =============神经网络用于回归=============

import numpy as np
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPRegressor  # 多层线性回归
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from CrawlerUtil import read_csv
from sklearn.metrics import mean_squared_error, r2_score,mean_absolute_error


def convert2class(y, dataNum):
    print(dataNum)
    for i in range(dataNum - 1):
        if y[i] == 0: y[i] = 0
        elif y[i] < 0: y[i] = -1
        else: y[i] = 1
    return y


if __name__ == "__main__":
    # 加载样本数据集
    n = 120
    csv_file = read_csv('C:/Users/yuzhe/Desktop/OptionAnalysis/files/files_'
                        + n.__str__()
                        + 'min/REDUCED_FEATURE_VECTOR_' + n.__str__() + '.csv')
    dataNum = len(csv_file)
    featureNum = len(csv_file[0])-1
    print("特征的维度", featureNum)
    dataMat = np.array(csv_file)
    X = dataMat[1:, 0:featureNum].astype(float)
    y = dataMat[1:, featureNum].astype(float)
    y = convert2class(y, dataNum) #转换为类别

    # 神经网络对数据尺度敏感，所以最好在训练前标准化，或者归一化，或者缩放到[-1,1]
    scaler = StandardScaler() # 标准化转换
    scaler.fit(X)  # 训练标准化对象
    X = scaler.transform(X)   # 转换数据集

    # 数据集分割
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

    # solver='lbfgs',  MLP的求解方法：L-BFGS 在小数据上表现较好，Adam 较为鲁棒，SGD在参数调整较优时会有最佳表现（分类效果与迭代次数）；SGD标识随机梯度下降。
    # alpha:L2的参数：MLP是可以支持正则化的，默认为L2，具体参数需要调整
    # hidden_layer_sizes=(5, 2) hidden层2层,第一层5个神经元，第二层2个神经元)，2层隐藏层，也就有3层神经网络
    clf = MLPRegressor(solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=1)
    clf.fit(X, y)

    # 对测试集进行预测
    y_pred = clf.predict(X_test)

    print("Mean Absolute error:", mean_absolute_error(y_test, y_pred))
    # The mean squared error
    print("Mean squared error:", mean_squared_error(y_test,y_pred))
    # Explained variance score: 1 is perfect prediction
    print('R2 score:', clf.score(X_test, y_test))

    '''
    cengindex = 0
    for wi in clf.coefs_:
        cengindex += 1  # 表示底第几层神经网络。
        print('第%d层网络层:' % cengindex)
        print('权重矩阵维度:',wi.shape)
        print('系数矩阵：\n',wi)
    '''
    # 显示测试集预测的结果的人民币汇率的涨跌趋势
    test_result = np.zeros(len(X_test), dtype=np.float64)

    for i in range(len(X_test)):
        if i == 0:
            test_result[i] = clf.predict(X_test[i].reshape(1, -1))
        else:
            test_result[i] = clf.predict(X_test[i].reshape(1, -1)) + test_result[i - 1]

    print('预测结果：\n', test_result)
    plt.figure(figsize=(12, 6))
    plt.title('result')
    plt.plot(np.arange(len(X_test)) + 1, test_result, 'r-',
             label='Test Set Result')
    plt.legend(loc='upper right')
    plt.xlabel('Test Sample')
    plt.ylabel('Growth Rate')
    plt.show()
