from numpy import *
import operator

def createDataSet():
    group = array([ 
        [1.0, 1.1], 
        [1.0, 1.0], 
        [0  , 0  ], 
        [0  , 0.1] 
    ])
    labels = ['A', 'A', 'B', 'B']
    return group,labels

def classify0(inX, dataSet, labels, k):
    '''
        inX 输入向量
        k 近邻数目
    '''
    #取得array的长度,列方向长度
    dataSetSize = dataSet.shape[0] 
    #inX向量填充列方向dataSetSize,行方向1   减法每个点互减
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    #每个点平方
    sqDiffMat = diffMat**2
    #axis=1 是按行求和 , axis=0是按列求和
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    #argsort函数返回的是数组值从小到大的索引值
    #一维 >>> x = np.array([3, 1, 2]) >>> np.argsort(x) 结果:array([1, 2, 0])
    #二维 axis=0 按列排序, axis=1 按行排序
    sortedDistIndicies = distances.argsort()
    #排序索引是为了关联labels
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.items(), key=lambda k:k[1], reverse=True)
    #[{'B':2},{'A':1}]
    print(sortedClassCount)
    return sortedClassCount[0][0]


# dataSet,labels = createDataSet()
# print(classify0([0.6,0.5], dataSet, labels, 3))


##############

'''一维数组  
zeros(3) 

二维数组  
zeros((2,3)) 
returnMat[index,:]=[1,2,3] 直接对行赋值,赋值的行不能超过初始化的
Mat[:,1] 取第二列的数据
'''
#Matplotlib 里的常用类的包含关系为 Figure -> Axes -> (Line2D, Text, etc.)
#一个Figure对象可以包含多个子图(Axes)，在matplotlib中用Axes对象表示一个绘图区域，可以理解为子图。
import matplotlib
import matplotlib.pyplot as plt
def ccc(dat):
    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.scatter(dat[:,0],dat[:,1])
    plt.show()

# import random
# size=100
# dat = zeros((size,2))
# for i in range(size):
#     x = random.random()
#     y = random.random()
#     dat[i,:] = [x,y]
# ccc(dat)

###############

def autoNorm(dateSet):
    '''归一化特征 newValue = (oldValue-min)/(max-min)'''
    # 各属性最小值和最大值各自组成
    dateSet=array([[1,2],[2,3],[3,4]])
    minVals = dateSet.min(0)
    maxVals = dateSet.max(0)
    ranges = maxVals - minVals
    # 返回矩阵的列行值
    normDateSet = zeros(shape(dateSet))
    m = dateSet.shape(0)
    normDateSet = dateSet - tile(minVals, (m,1))
    normDateSet = normDateSet/tile(ranges, (m,1))
    return normDateSet, ranges, minVals