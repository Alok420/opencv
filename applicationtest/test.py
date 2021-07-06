import cv2 as cv
# img=cv.imread("DSC_0651.JPG");
# cv.imshow("Heart",img);
def resized(frame, scale=.2):
    heaght = int(frame.shape[0] * scale)
    width = int(frame.shape[1] * scale)
    return cv.resize(frame, (width, heaght), interpolation=cv.INTER_AREA)


capture = cv.VideoCapture("video/water.mp4")  # pass 0 for camera 1 or 2 for second camera else path for stored video
count = 0
while True:
    count += 1
    isTrue, frame = capture.read()
    # resized_frame=resized(frame,.5)
    cv.imwrite("frame_images/frame%d.jpg" % count, frame)  # this will write every frames in a folder
    cv.imshow("Vid", frame)
    # cv.imshow("Scaled frame",resized_frame)
    if cv.waitKey(20) & 0xff == ord('d'):  # this will wait for key press d
        break
capture.release()
cv.destroyAllWindows()
