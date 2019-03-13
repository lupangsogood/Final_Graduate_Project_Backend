import cv2
import numpy as np
import dlib
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

#im_bg = cv2.imread('S__39534597.jpg')
im_bg = cv2.imread('input7.jpg')
#READ IMAGE LIKE TRANsPARENT Background
im_fg = cv2.imread('testjangmakL1.jpg',flags=cv2.IMREAD_UNCHANGED)
#im_fg = cv2.imread('bgwhiteL1.jpg')


imROI = im_bg.copy()
imOrg = im_bg.copy()

imOrg = cv2.resize(imOrg,(750,1000))
gray = cv2.cvtColor(imOrg,cv2.COLOR_BGR2GRAY)
rects = detector(gray,1)
for (i,rect) in enumerate(rects):
    shape = predictor(gray,rect)

    #ค่าความกว้างของหน้า และ ความสูงของหน้า
    HALF_FACE_RATIO = (1.0/15)
    halfFace = (shape.part(16).x * HALF_FACE_RATIO)/3
    faceWidth = shape.part(16).x
    FACE_HEIGHT_RATIO = (1.0 / 6)
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

ROI_BGR  = imOrg[yR:hR+4,xR:wR-10]
ROI_GRAY = cv2.cvtColor(ROI_BGR,cv2.COLOR_BGR2GRAY)
cv2.imshow("TEST_GRAY",ROI_GRAY)
cv2.waitKey(0)

ROI_GET_COLOR = imOrg[yR-50:hR-30,xR+20:wR]
#cv2.imshow("ROI_GET_COLOR",ROI_GET_COLOR)
#cv2.waitKey(0)
### หาค่าสีของเส้นบนคิ้วแต่ละจุด
eyeBrown_color = []
eyeBrown_color =[(gray[shape.part(17).x,shape.part(17).y]),(gray[shape.part(18).x,shape.part(18).y]),(gray[shape.part(19).x,shape.part(19).y]),(gray[shape.part(20).x,shape.part(20).y]),(gray[shape.part(21).x,shape.part(21).y])]
BGR_AVG = sum (eyeBrown_color)/len(eyeBrown_color)
print (BGR_AVG)

###ส่วนจัดการลูป REPLACE COLOR PIXEL
get_color = (ROI_GET_COLOR[25,25])
#print(get_color)
height,width = ROI_BGR.shape[:2]
print ("WIDTH,HEIGHT = ",width,height)


#cv2.imshow("ROI_GRAY",imOrg)
#cv2.waitKey(0)
im_bg = imOrg.copy()
#---------------------------------------------------------------------------
im_fg = cv2.resize(im_fg,(int(((wR-xR)+halfFace)),int(((hR-yR)+heightFace))))
print ("FACE WIDTH = ",im_fg.shape[:2])
#im_fg= cv2.GaussianBlur(im_fg,(1,1),5)
#im_fg = cv2.resize(im_fg,(100,100))
mask = 255 * np.ones(im_fg.shape, im_fg.dtype)

bg_width, bg_height, bg_channels = im_bg.shape
#center = (int(bg_height/2), int(bg_width/2))
point = (int((xR+wR)/2),int((yR+hR)/2))
#print(center)
#print(point)
mixed_clone = cv2.seamlessClone(im_fg, im_bg, mask,point, cv2.MIXED_CLONE)
#mixed_clone_2 = cv2.seamlessClone(im_fg, imOrg, mask,point, cv2.MIXED_CLONE)
print ("XR = , YR  = ,WR = ,HR = ",xR,yR,wR,hR)
cv2.circle(mixed_clone,point, 5, (0,255,0), -1)
cv2.imshow("ROI_GRAY",mixed_clone)
cv2.waitKey(0)

###---------ทดสอบการ REPLACE สี
"""
for w in range(width):
    for h in range(height):
        print (w,h)
        # ความสูงมาก่อน
        color_gray = ROI_GRAY[h,w]
        #print (color_gray)

        if color_gray < (BGR_AVG/2):
            print("CHECKED")
            ROI_BGR[h,w] = get_color
"""