# 导入所需工具包
from pyzbar import pyzbar
import argparse
import datetime
import time
import cv2
import numpy as np
from PIL import Image

def decodeDisplay(image):
    barcodes = pyzbar.decode(image)
    for barcode in barcodes:
        # 提取二维码的边界框的位置
        # 画出图像中条形码的边界框
        #(x, y, w, h) = barcode.rect
        #print(x+w,y+h,x,y,image.shape)
        #cv2.rectangle(image, (x, y), (x + w, y + h), (225, 225, 225), 2)
        pointss =[]
        for point in barcode.polygon:
            pointss.append([point[0], point[1]])
        pointss = np.array(pointss,dtype=np.int32).reshape(-1,1, 2)
        cv2.polylines(image, [pointss], isClosed=True, color=(0,0,255),thickness=2)
        print(pointss)
        # 提取二维码数据为字节对象，所以如果我们想在输出图像上
        # 画出来，就需要先将它转换成字符串
        #barcodeData = barcode.data.decode("utf-8")
        #barcodeType = barcode.type

        # 绘出图像上条形码的数据和条形码类型
        #text = "{} ({})".format(barcodeData, barcodeType)
        #cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 225), 2)
        # 向终端打印条形码数据和条形码类型
    return image,pointss[0][0][0],pointss[0][0][1],pointss[2][0][0],pointss[2][0][1]



filename="22.jpeg"
image = cv2.imread(filename)
im,a,b,c,d = decodeDisplay(image)
print(a,b,c,d)
img = Image.open(filename)
print(img.size) #(1920, 1080)
cropped = img.crop((a,b,c,d))  # (left, upper, right, lower)
cropped.save("pil_cut_thor.jpg")