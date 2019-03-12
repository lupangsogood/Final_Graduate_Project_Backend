import cv2
import numpy as np
import dlib
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

im_bg = cv2.imread('Input3.jpg')
#READ IMAGE LIKE TRANsPARENT Background
#im_fg = cv2.imread('bggray.jpg',flags=cv2.IMREAD_UNCHANGED)
im_fg = cv2.imread('bgwhite.jpg',flags=cv2.IMREAD_UNCHANGED)
#im_fg = cv2.resize(im_fg,(100,100))
#COPY IM_BG TO IMORG
imOrg = im_bg.copy()

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
    yR = shape.part(19).y-10
    wR = shape.part(21).x
    hR = shape.part(19).y+30
    cv2.rectangle(imOrg,(xR,yR),(wR,hR),(255,86,30),3)

    xL = shape.part(22).x
    yL = shape.part(24).y-10
    wL = shape.part(26).x
    hL = shape.part(24).y+30
    cv2.rectangle(imOrg,(xL,yL),(wL,hL),(255,86,30),3)

    #cv2.imshow("ROI",imOrg)
    #cv2.waitKey(0)

#เทสตำแหน่ง width , height ของ Graphic ให้สอดคล้องกับขนาด Bound คิ้ว
im_fg = cv2.resize(im_fg,(int(wR/3),int(hR/3)))
print(im_fg.shape[:])
mask = 255 * np.ones(im_fg.shape, im_fg.dtype)

# The location of the center of the IM_FG in the IM_BG
width, height, channels = im_bg.shape
#ลองเปลี่ยนจากขนาดของหน้าเป็นขนาด ROI คิ้ว
center = (int(height/2), int(width/2))
point = (int((xR+wR)/2),int((yR+hR)/2))
#print(center)
print(point)


# Seamlessly clone src into dst and put the results in output
mixed_clone = cv2.seamlessClone(im_fg, im_bg, mask,point, cv2.MIXED_CLONE)
#TEST POINT BY CIRCLE
mixed_clone = cv2.circle(mixed_clone,point,3,(255,0,0),-1)
# Write results
cv2.imshow("MIXED",mixed_clone)
cv2.waitKey(0)