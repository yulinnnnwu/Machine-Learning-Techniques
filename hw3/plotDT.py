import matplotlib.pyplot as plt
# 解决画图中文字符显示异常的问题
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

# 用来计算叶子数
def getNumLeafs(myTree):
    if len(myTree.val) == 1:
        return 1
    if myTree == None:
        return 0

    return getNumLeafs(myTree.left) + getNumLeafs(myTree.right)

# 计算树的深度
def getTreeDepth(myTree):
    if myTree == None:
        return 0

    depth = max(1 + getTreeDepth(myTree.left),\
                1 + getTreeDepth(myTree.right))
    return depth

decisionNode = dict(boxstyle="sawtooth", fc="5")
leafNode = dict(boxstyle="round4", fc="5")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt,\
    xycoords='axes fraction',\
    xytext=centerPt, textcoords='axes fraction', \
    va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)


def createPlot():
    fig = plt.figure(facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode('决策节点', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('叶节点', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()


def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0]-cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1]-cntrPt[1])/2.0 + cntrPt[1]
    createPlot.ax1.text(xMid, yMid, txtString, va="center", ha="center", rotation=30)


def plotTree(myTree, parentPt, nodeTxt):#if the first key tells you what feat was split on
    numLeafs = getNumLeafs(myTree)  #this determines the x width of this tree
    depth = getTreeDepth(myTree) - 1
    #this determines the x width of this tree
    cntrPt = (1.2 * (plotTree.xOff + (1.0 + float(numLeafs))/2.0/plotTree.totalW), 1.2 * plotTree.yOff)

    if len(myTree.val) > 1 and myTree.val['theta'] != -1:
        plotMidText(cntrPt, parentPt, nodeTxt)
        plotNode("feature:"+str(myTree.val['feature'])\
                 +"\nVal:"+str(round(myTree.val['theta'],2))\
                 +"\nGini:"+str(round(myTree.val['Gini'],2))\
                 +"\ns:"+str(myTree.val['s']), \
                 cntrPt, parentPt, decisionNode)
        plotTree.yOff = plotTree.yOff - 2/plotTree.totalD
    else:
        plotTree.xOff = plotTree.xOff + 1/plotTree.totalW
        plotMidText(cntrPt, parentPt, nodeTxt)
        plotNode(str(myTree.val['leaf']), cntrPt, parentPt, decisionNode)
        plotTree.yOff = plotTree.yOff - 2/plotTree.totalD

    if myTree.left != None:
        plotTree(myTree.left,cntrPt, "小于")
    if myTree.right != None:
        plotTree(myTree.right,cntrPt,"大于等于")

    plotTree.yOff = plotTree.yOff + 2/plotTree.totalD


def createPlot(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlot.ax1 = plt.subplot(111, frameon=False, **axprops)    #no ticks
    #createPlot.ax1 = plt.subplot(111, frameon=False) #ticks for demo puropses
    plotTree.totalW = float(getNumLeafs(inTree))
    plotTree.totalD = float(getTreeDepth(inTree) - 1)
    plotTree.xOff = -0.5/plotTree.totalW; plotTree.yOff = 1.0;
    plotTree(inTree, (0.5,1.0), '')
    plt.show()
