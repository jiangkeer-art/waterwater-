# 导入所需工具包
from imutils.video import VideoStream
from pyzbar import pyzbar
import argparse
import datetime
import imutils
import time
import cv2

# 创建参数解析器，解析参数
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", type=str, default="barcodes.csv",
    help="path to output CSV file containing barcodes")
args = vars(ap.parse_args())
# 初始化视频流
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# 打开输出CSV文件，用来写入和初始化迄今发现的所有条形码
csv = open(args["output"], "w")
found = set()
# 循环来自视频流的帧
while True:
# 抓取视频流的帧
    # 将大小重新调整为最大宽度400像素
    frame = vs.read()
    frame=imutils.resize(frame,width=400)

    # 找到视频中的条形码，并解析所有条形码
    barcodes = pyzbar.decode(frame)
    # 循环检测到的条形码
    for barcode in barcodes:
        # 提取条形码的边界框位置
        # 绘出围绕图像上条形码的边界框
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame,(x, y),(x+ w, y + h),(0,0,255), 2)
        cropped = frame[x+w:y+h,x:y]  # 裁剪坐标为[y0:y1, x0:x1]
        if cropped.size != 0:
            cv2.imwrite('cv_cut_thor.jpg', cropped)
        # 条形码数据为字节对象，所以如果我们想把它画出来
        # 需要先把它转换成字符串
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # 绘出图像上的条形码数据和类型
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        # 如果条形码文本目前不在CSV文件中, 
        # 就将时间戳+条形码 写入硬盘并更新集合
        if barcodeData not in found:
            csv.write("{},{}\n".format(datetime.datetime.now(),
                barcodeData))
            csv.flush()
            found.add(barcodeData)
	# 展示输出帧
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    # 如果按下”q”键就停止循环
    if key == ord("q"):
        break

# 关闭输出CSV文件进行清除
print("[INFO] cleaning up...")
csv.close()
cv2.destroyAllWindows()
vs.stop()
