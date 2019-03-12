import cv2
import numpy as np
import dlib
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

im_bg = cv2.imread('Input6.jpg')
#READ IMAGE LIKE TRANsPARENT Background
im_fg = cv2.imread('bgwhite.jpg',flags=cv2.IMREAD_UNCHANGED)

#COPY IM_BG TO IMOrg
imROI = im_bg.copy()
imOrg = im_bg.copy()

imOrg = cv2.resize(imOrg,(750,1000))
gray = cv2.cvtColor(imOrg,cv2.COLOR_BGR2GRAY)
rects = detector(gray,1)
for (i,rect) in enumerate(rects):
    shape = predictor(gray,rect)

    #ค่าความกว้างของหน้า และ ความสูงของหน้า
    HALF_FACE_RATIO = (0.695)
    halfFace = shape.part(16).x * HALF_FACE_RATIO
    FACE_HEIGHT_RATIO = (1.0 / 5)
    heightFace = shape.part(8).y * FACE_HEIGHT_RATIO

    #ค่าจุดกลางของหน้าเอาไว้จุดแก้มอีกหนึ่งข้าง
    mid = shape.part(33).x-20

    xR = shape.part(17).x
    yR = shape.part(19).y
    wR = shape.part(21).x
    hR = shape.part(17).y

    xL = shape.part(22).x
    yL = shape.part(24).y-10
    wL = shape.part(26).x
    hL = shape.part(24).y+30

    #cv2.imshow("ROI",imOrg)
    #cv2.waitKey(0)

ROI = imROI[yR:hR,xR+10:wR]
mask_ROI = 255 * np.ones(ROI.shape, ROI.dtype)

ROI_FOREHEAD =imOrg[yR+5:hR+5,xR:wR]
cv2.imshow("ROI_FOREHEAD",ROI_FOREHEAD)
cv2.waitKey(0)
#--------------------------------------------------------------
#color = (ROI_FOREHEAD[0,0])
#print(color)
#---------------------------------------------------------------
ROI_FOREHEAD= cv2.GaussianBlur(ROI_FOREHEAD,(3,3),5)
#ROI_FOREHEAD = cv2.bilateralFilter(ROI_FOREHEAD,55,55,55)
imOrg[yR:hR,xR:wR] = ROI_FOREHEAD
cv2.imshow("ROI_FOREHEAD",imOrg)
cv2.waitKey(0)
#-----------เซต IM_BG ให้เท่ากับ ภาพที่เบลอคิ้วแล้ว
im_bg = imOrg.copy()
#-------------------------------

im_fg = cv2.resize(im_fg,(int((wR+xR)*0.175),int((hR+yR)*0.15)))

print(im_fg.shape[:])
mask = 255 * np.ones(im_fg.shape, im_fg.dtype)

# The location of the center of the IM_FG in the IM_BG
width, height, channels = im_bg.shape
#ลองเปลี่ยนจากขนาดของหน้าเป็นขนาด ROI คิ้ว
center = (int(height/2), int(width/2))
point = (int((xR+wR)/1.95),int((yR+hR)/2))
#print(center)
print(point)

# Seamlessly clone src into dst and put the results in output
mixed_clone = cv2.seamlessClone(im_fg, im_bg, mask,point, cv2.MIXED_CLONE)

# Write results
cv2.imshow("MIXED",mixed_clone)
cv2.waitKey(0)

