import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from PIL import Image
from djitellopy import Tello
import  time
import  math

# CONNECT TO TELLO
me = Tello()
me.connect()
me.for_back_velocity = 0
me.left_right_velocity = 0
me.up_down_velocity = 0
me.yaw_velocity = 0
me.speed = 0

print(me.get_battery())

me.streamoff()
me.streamon()

def decodeQr():
    image = cv2.imread("./image/demo.jpeg")
    decodedObjects = pyzbar.decode(image)
    print(decodedObjects)
    for obj in decodedObjects:
        print("Type:", obj.type)
        print("Data: ", obj.data, "\n")
    cv2.imshow("image",image)
    cv2.waitKey(0)

def distance(List): #計算與中間點之距離

    # List[0][0] +
    # for point in List:    #先找到中間點

    print(len(List))
    middlePoint = [(List[0][0] + List[2][0])/2,  (List[0][1] + List[2][1])/2] #TODO: 回傳中心點
    disToMiddle =  math.sqrt((480 - middlePoint[0])**2 + (360 - middlePoint[1])**2)
    # print(math.sqrt((480 - (List[0][0] + List[2][0])/2)**2) , (List[0][1] + List[2][1])/2)

    return [middlePoint,disToMiddle]

def drawPolyGon(positions, frame):

    list = [] #所有的Point
    minDinstance = 1000
    middleQRcode = [] #存放middlepoint

    for pos in positions:  #所有的QR code
        red = 0
        green = 0
        pList = [] #單次的Point四點
        for i in range(4): #QR code四個點
            pList.append([pos.polygon[i].x, pos.polygon[i].y])
            cv2.circle(frame, (pos.polygon[i].x, pos.polygon[i].y), 5, (255, 0, 0), -1) #draw circle points
            cv2.putText(frame,str([pos.polygon[i].x, pos.polygon[i].y]) + str(i), (pos.polygon[i].x - 10, pos.polygon[i].y - 10)
                        , cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
        print(distance(pList)) #TODO: 1.把取回來的MidPoint畫上去QRcode 2.排序Distance去抓最中間的QRcode用紅框標示出來
        eachPoint = distance(pList)
        cv2.circle(frame, (int(eachPoint[0][0]), int(eachPoint[0][1])), 5, (255, 0, 0), -1) #Draw Middle Point
        cv2.putText(frame, str(round(eachPoint[1],2)) + str(i),
                    (int(eachPoint[0][0]) - 10, int(eachPoint[0][1]) - 10)
                    , cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 1, cv2.LINE_AA)
        # cv2.circle(frame, (pos.polygon[i].x, pos.polygon[i].y), 5, (255, 0, 0), -1)


        if(eachPoint[1] < minDinstance):
            minDinstance = eachPoint[1]
            middleQRcode = pList   #紀錄最中間的座標


        # Calculate Distance
        list.append(pList)
        pts = np.array(pList, np.int32)
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts], True, (0, 255, 0))

    pts = np.array(middleQRcode, np.int32)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], True, (0, 0, 255))
    return frame

def streamDecode():
    frame_read = me.get_frame_read()

    # cap = cv2.VideoCapture(0)

    while True:
        # _, frame = cap.read()
        myFrame = frame_read.frame
        recFrame = myFrame  # copy origin frame
        decodeObjects = pyzbar.decode(myFrame)  # decode QRcode

        if decodeObjects:
            print(decodeObjects)
            recFrame = drawPolyGon(decodeObjects, recFrame)

            # print(drawPolyGon(decodeObjects, recFrame))
            # for obj in decodeObjects:
            #     print("QrCode Position: ", obj.polygon[1].x)
        cv2.circle(recFrame, (480, 360), 5, (255, 0, 0), -1)  # draw circle points
        cv2.imshow("Frame", recFrame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:  # Esc
            break

if __name__ == '__main__':
    #decodeQr()
    streamDecode()
