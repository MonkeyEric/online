# coding:utf-8
import matplotlib.pyplot as plt
import pylab
img_arr = plt.imread('./lufei.jpeg') # 将图片数据读取到数组中
print(img_arr) # 三维数组，分别是 长、宽、颜色
# 通过数组，将图片显示出来
plt.imshow(img_arr)
pylab.show()
# 修改图片的原始数据，将每一个数组元素减去100 
# plt.imshow(img_arr-100)