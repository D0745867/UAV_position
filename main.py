from djitellopy import Tello
import cv2
import numpy as np
import time
######################################################################
width = 640  # WIDTH OF THE IMAGE
height = 480  # HEIGHT OF THE IMAGE
startCounter =0   #  0 FOR FIGHT 1 FOR TESTING
######################################################################


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

while True:

    # GET THE IMGAE FROM TELLO
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    img = cv2.resize(myFrame, (width, height))

    cv2.imshow("MyResult", img)
    # TO GO UP IN THE BEGINNING
    # if startCounter == 0:
    #     me.takeoff()
    #     time.sleep(8)
    #     me.rotate_clockwise(90)
    #     time.sleep(3)
    #     me.move_left(35)
    #     time.sleep(3)
    #     me.land()
    #     startCounter = 1

    # # SEND VELOCITY VALUES TO TELLO
    # if me.send_rc_control:
    #     me.send_rc_control(me.left_right_velocity, me.for_back_velocity, me.up_down_velocity, me.yaw_velocity)

    # DISPLAY IMAGE


    # WAIT FOR THE 'Q' BUTTON TO STOP
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break

#######QRcode#########

inputImage = cv2.imread("./image/youtube.jpeg")

# Display barcode and QR code location
def display(im, bbox):
    n = len(bbox)
    for j in range(n):
        cv2.line(im, tuple(bbox[j][0]), tuple(bbox[ (j+1) % n][0]), (255,0,0), 3)

    # Display results
    cv2.imshow("Results", im)

# Create a qrCodeDetector Object
qrDecoder = cv2.QRCodeDetector()

# Detect and decode the qrcode
t = time.time()
data,bbox,rectifiedImage = qrDecoder.detectAndDecode(frame_read)
print("Time Taken for Detect and Decode : {:.3f} seconds".format(time.time() - t))
if len(data)>0:
    print("Decoded Data : {}".format(data))
    display(inputImage, bbox)
    rectifiedImage = np.uint8(rectifiedImage);
    cv2.imshow("Rectified QRCode", rectifiedImage);
else:
    print("QR Code not detected")
    cv2.imshow("Results", frame_read)
cv2.imwrite("output.jpg",frame_read)
cv2.waitKey(0)
cv2.destroyAllWindows()