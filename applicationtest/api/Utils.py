import cv2
import os
import numpy as np
import imutils as imutils
import natsort


class Utils:
    def getCountours(self,img, cThr=[100, 100], showCanny=False, minArea=1000, filter=0, draw=False, isSecondRound=False, isSorted=True):
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)
            imgCanny = cv2.Canny(imgBlur, cThr[0], cThr[1])
            kernal = np.ones((5, 5))
            imgDialate = cv2.dilate(imgCanny, kernal, iterations=3)
            imgThres = cv2.erode(imgDialate, kernal, iterations=2)
            if showCanny:
                cv2.imshow("Canny", imgCanny)
            if isSecondRound:
                contours, hierarchy = cv2.findContours(
                    imgThres, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            else:
                contours, hierarchy = cv2.findContours(
                    imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            gcontour = []
            for i in contours:
                if isSecondRound:
                    x, y, w, h = cv2.boundingRect(i)
                    # cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    M = cv2.moments(i)
                    cX = int(M["m10"] / M["m00"])
                    cY = int(M["m01"] / M["m00"])
                    b, g, r = (img[cY, cX])
                else:
                    r = 1
                    g = 1
                    b = 1
                area = cv2.contourArea(i)
                if area > minArea:
                    peri = cv2.arcLength(i, True)
                    approx = cv2.approxPolyDP(i, 0.02 * peri, True)
                    bbox = cv2.boundingRect(approx)
                    if filter > 0:
                        # if len(approx) == filter:
                        gcontour.append([len(approx), area, approx,bbox, i, (r, g,b),peri])
                    else:
                        gcontour.append([len(approx), area, approx, bbox, i,(r, g,b),peri])
            if isSorted:
                gcontour = sorted(gcontour, key=lambda x: x[1], reverse=True)
            if draw:
                a=0
                for con in gcontour:
                    a+=1
                    cv2.drawContours(img, con[4], -1, (0, 0, 255), 2)
                    x, y, w, h = cv2.boundingRect(con[4])
                    cv2.putText(img, str(con[1]), (x, y),cv2.FONT_HERSHEY_SIMPLEX, 0.4, (1, 1, 1), 1)
            return img, gcontour

    def getDirFiles(self,dir="applicationtest/static/images/"):
        print(dir)
        listpath = os.listdir(dir)
        listpath = natsort.natsorted(listpath, reverse=False)
        return listpath


    def reOrder(self,myPoints):
        # print("shaped points", myPoints.shape)
        myNewPoints = np.zeros_like(myPoints)
        myPoints = myPoints.reshape(4, 2)
        add = myPoints.sum(1)
        myNewPoints[0] = myPoints[np.argmin(add)]
        myNewPoints[3] = myPoints[np.argmax(add)]
        diff = np.diff(myPoints, axis=1)
        myNewPoints[1] = myPoints[np.argmin(diff)]
        myNewPoints[2] = myPoints[np.argmax(diff)]
        return myNewPoints


    def warpImage(self,img, points, w, h, pad=8):
        # print("points", points)
        points = self.reOrder(points)
        # print("reorder points", points)
        pts1 = np.float32(points)
        pts2 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarp = cv2.warpPerspective(img, matrix, (w, h))
        imgWarp = imgWarp[pad:imgWarp.shape[0] - pad, pad:imgWarp.shape[1] - pad]
        return imgWarp


    def colored(self,r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


    def getRGBColor(img, contours):
        colors = []
        for c in contours:
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            b, g, r = (img[cY, cX])
            colors.append((r, g, b))
        return colors
