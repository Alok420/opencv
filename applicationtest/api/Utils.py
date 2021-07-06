import cv2
import os
import numpy as np
import imutils as imutils
import natsort


class Utils:
    def getCountours(self,img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False):
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
        imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
        kernal = np.ones((5, 5))
        imgDialate = cv2.dilate(imgCanny, kernal, iterations=3)
        imgThres = cv2.erode(imgDialate, kernal, iterations=2)
        if showCanny:
            cv2.imshow("Canny", imgThres)
        contours, hierarchy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
       
        gcontour = []
        for i in contours:
            M = cv2.moments(i)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # return str(cX)+"---"+str(cY)
            # exit 
            b, g, r = (img[cX, cY])
            area = cv2.contourArea(i)
            if area > minArea:
                peri = cv2.arcLength(i, True)
                approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                # print("lenth is:{}".format(len(approx)))
                bbox = cv2.boundingRect(approx)
                if filter > 0:
                    # if len(approx) == filter:
                    gcontour.append(
                        [len(approx), area, approx, bbox, i, (r, g, b)])
                else:
                    gcontour.append(
                        [len(approx), area, approx, bbox, i, (r, g, b)])
        gcontour = sorted(gcontour, key=lambda x: x[1], reverse=True)
        if draw:
            for con in gcontour:
                cv2.drawContours(img, con[4], -1, (0, 0, 255), 2)
        return img, gcontour

    def getDirFiles(self,dir="applicationtest/static/images/"):
        listpath = os.listdir(dir)
        listpath = natsort.natsorted(listpath, reverse=False)
        return listpath

    def reOrder(self,myPoints):
        print("shaped points", myPoints.shape)
        myNewPoints = np.zeros_like(myPoints)
        myPoints = myPoints.reshape(4, 2)
        add = myPoints.sum(1)
        myNewPoints[0] = myPoints[np.argmin(add)]
        myNewPoints[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis=1)
        myNewPoints[1] = myPoints[np.argmin(diff)]
        myNewPoints[2] = myPoints[np.argmax(diff)]
        return myNewPoints

    def warpImage(self,img, points, w, h, pad=20):
        print("points", points)
        points = self.reOrder(points)
        print("reorder points", points)
        pts1 = np.float32(points)
        pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(img, matrix, (w, h))
        imgWarp = imgWarp[pad:imgWarp.shape[0]-pad, pad:imgWarp.shape[1]-pad]
        return imgWarp

    def RGB2HEX(self,color):
        return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

    def getRGBColor(self,img, contours):
        colors = []
        for c in contours:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            b, g, r = (img[cX, cY])
            colors.append((r, g, b))
        return colors
