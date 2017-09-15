from math import log
import operator

def createDataSet():
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing','flippers']
    return dataSet, labels

def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    #统计分类出现
    for featVec in dataSet:
        currentLabel = featVec[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEnt = 0
    #计算信息期望
    for key in labelCounts:
        #分类概率
        prob = labelCounts[key]/numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt

def splitDataSet(dataSet, axis, value):
    #axis特征,value特征值
    retDataSet = []
    for featVec in dataSet:
        #去除这个特征,返回符合这个特征值的集合
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis+1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    #取类别数量
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    #遍历分类
    for i in range(numFeatures):
        #整个分类的特征值列表
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        #取特征,分别计算熵
        for value in uniqueVals:
            #分离特征集合
            subDataSet = splitDataSet(dataSet, i, value)
            #特征分类概率
            prob = len(subDataSet)/len(dataSet)
            newEntropy += prob * calcShannonEnt(subDataSet)
        #信息增益是熵的减少
        infoGain = baseEntropy - newEntropy
        if(infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(),key=lambda k:k[1],reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet,labels):
    #分类列表
    classList = [example[-1] for example in dataSet]
    #出口1,分类相同
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    #出口2,遍历完特征,还存在不同分类,多数决定
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel:{}}
    del(labels[bestFeat])
    #最优特征的值列表
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    #分支
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet,bestFeat,value),subLabels)
    return myTree

def classify(inputTree,featLabels,testVec):
    #{'no surfacing':{0:'no',1:{'flippers':{0:'no',1:'yes'}}}}
    #获得树的第一特征
    firstStr = list(inputTree.keys())[0]
    #第一特征对应的字典
    secondDict = inputTree[firstStr]
    #找到特征对应测试的下标
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]) == 'dict':
                classLabels = classify(secondDict[key],featLabels,testVec)
            else:
                classLabels = secondDict[key]
    return classLabels

def storeTree(inputTree, filename):
    import pickle
    fw = open(filename,'w')
    pickle.dump(inputTree,fw)
    fw.close()

def grabTree(filename):
    import pickle
    fr = open(filename)
    return pickle.load(fr)

#########################
# import matplotlib.pyplot as plt 

# decisionNode = dict(boxstyle='sawtooth', fc='0.8')
# leafNode = dict(boxstyle='round4', fc='0.8')
# arrow_args = dict(arrowstyle='<-')

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt,
        textcoords='axes fraction',va='center',ha='center',bbox=nodeType,arrowprops=arrow_args)
def createPlot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode('a decision node', (0.5,0.1), (0.1,0.5), decisionNode)
    plotNode('a leaf node', (0.8,0.1), (0.3,0.8),leafNode)
    plt.show()

#########################



