import cv2
import numpy as np
import dlib
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

<<<<<<< HEAD
dst = cv2.imread('../FILE_OUTPUT_color_207_40_57.jpg')
src = cv2.imread('eyebrowL.png')

height,width,depth = src.shape
circle_img = np.zeros((height,width),np.uint8)
cv2.circle(circle_img,(int(width/2),int(height/2)),280,1,thickness=-1)
mask_data = cv2.bitwise_and(src,src,mask=circle_img)

cv2.imshow("MASK",mask_data)
cv2.waitKey(0)

#cv2.imshow("DISPLAY",out)
#cv2.waitKey(0)

"""
cv2.imshow('Original',img)
cv2.waitKey(0)
## For Specs

imOrg = img.copy()
=======
im_bg = cv2.imread('../FILE_OUTPUT_color_207_40_57.jpg')
#READ IMAGE LIKE TRANsPARENT Background
#im_fg = cv2.imread('bggray.jpg',flags=cv2.IMREAD_UNCHANGED)
im_fg = cv2.imread('bgwhite.jpg',flags=cv2.IMREAD_UNCHANGED)
im_fg = cv2.resize(im_fg,(100,100))
#COPY IM_BG TO IMORG
imOrg = im_bg.copy()
>>>>>>> 25cae1a2d24eff44afebee126f38092f51d257be
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
    x = shape.part(17).x
    y = shape.part(19).y-10
    w = shape.part(21).x+10
    h = shape.part(19).y+30
    cv2.rectangle(imOrg,(x,y),(w,h),(255,86,30),3)
<<<<<<< HEAD
=======
    
    cv2.imshow("ROI",imOrg)
    cv2.waitKey(0)

mask = 255 * np.ones(im_fg.shape, im_fg.dtype)

# The location of the center of the IM_FG in the IM_BG
width, height, channels = im_bg.shape
center = (int(height/2), int(width/2))
point = (int((x+w)/2),int((y+h)/2))
#print(center)
print(point)


# Seamlessly clone src into dst and put the results in output
mixed_clone = cv2.seamlessClone(im_fg, im_bg, mask,point, cv2.MIXED_CLONE)
#TEST POINT BY CIRCLE
mixed_clone = cv2.circle(mixed_clone,point,3,(255,0,0),-1)
# Write results
cv2.imshow("MIXED",mixed_clone)
cv2.waitKey(0)






"""


>>>>>>> 25cae1a2d24eff44afebee126f38092f51d257be
"""