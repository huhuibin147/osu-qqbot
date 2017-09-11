from pylab import *
import numpy as np

figure(figsize=(8,6),dpi=80)

# subplot(numRows, numCols, plotNum) 例221,分成2*2绘制第1块
subplot(2,2,3)
x = np.linspace(-np.pi,np.pi,256,endpoint=True)
c = np.sin(x)
plot(x,c,color="blue",linewidth=1.0,linestyle="-")

subplot(2,2,2)
c = np.cos(x)
plot(x,c,color="red",linewidth=1.0,linestyle="-")

show()


