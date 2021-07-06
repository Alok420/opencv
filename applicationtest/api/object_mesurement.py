import cv2
import imutils as imutils

import utils;
from sklearn.cluster import KMeans
import os
webcame = False
path = "frame_images/frame1215.jpg"
cap = cv2.VideoCapture(0)
cap.set(10, 160)
cap.set(3, 1500)
cap.set(4, 1080)
isFirst = True
scale=1
paper_width = 210*scale
paper_heaight = 297*scale
while True:
    if webcame:
        success, img = cap.read()
    else:
        img = cv2.imread(path)
    resized = cv2.resize(img, (500, 500), fx=0.5, fy=0.5)
    img, gcontour = utils.getCountours(resized, showCanny=False, draw=True, minArea=0, filter=4)
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",len(gcontour))
    if len(gcontour) != 0:
        biggest = gcontour[0][2]
        area = gcontour[0][1]
        # smaller = gcontour[1][2]
        # area2 = gcontour[1][1]
        if isFirst:
            # print("--------------------")
            # print("*****")
            # print(area)
            # print("--------------------")
            # print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            # print("--------------------")
            # print(smaller)
            # print("*****")
            # print(area2)
            # print("--------------------")
            # print(biggest)
            warp_image=utils.warpImage(img,biggest,paper_width,paper_heaight)
            img2, gcontour2 = utils.getCountours(warp_image, showCanny=False, draw=True, minArea=0, filter=12)
            print("Gcontours2 ",len(gcontour2))
            if len(gcontour2) != 0:
                biggest2 = gcontour2[0][2]
                area2 = gcontour2[0][1]
                color=gcontour2[0][5]
                print("Area biggest ",area2)
                print("circle biggest",biggest2)
                print("Color biggest",color)

                    # cv2.polylines(img2,[obj[2]],True,(0,255,0),2)
        isFirst = False
    # cv2.imshow("warp_image",warp_image)
    # cv2.imshow("New Window", img)

    cv2.imshow("New Window", img2)
    if cv2.waitKey(20) & 0xff == ord('d'):  # this will wait for key press d
        break
