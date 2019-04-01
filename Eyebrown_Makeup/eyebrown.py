import cv2
import numpy as np
import dlib
import PIL
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

class Eyebrown_Makeup_class():
    
    def __init__(self):
        self.im = 0

    def apply_Eyebrown(self,imgBackground,imgEyeBrownRight,imgEyeBrownLeft):
        detector  = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        #im_bg = cv2.imread('S__39534597.jpg')
        #im_bg = cv2.imread('C:\\Users\\ANUSIT\\Documents\\GitHub\\Project_senior\\input1.jpg')
        #READ IMAGE LIKE TRANsPARENT Background
        #im_EyeBrown_Right = cv2.imread('C:\\Users\ANUSIT\\Documents\\GitHub\\Project_senior\\drawable\\testjangmakL1.jpg',flags=cv2.IMREAD_UNCHANGED)
        #im_fg = cv2.imread('bgwhiteL1.jpg')
        #im_EyeBrown_LEFT = cv2.imread('C:\\Users\ANUSIT\\Documents\\GitHub\\Project_senior\\drawable\\bgwhiteL1.jpg',flags=cv2.IMREAD_UNCHANGED)
        im_bg = cv2.imread(imgBackground)
        im_EyeBrown_Right = cv2.imread(imgEyeBrownRight,flags=cv2.IMREAD_UNCHANGED)
        im_EyeBrown_LEFT = cv2.imread(imgEyeBrownLeft,flags=cv2.IMREAD_UNCHANGED)

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
            yL = shape.part(24).y
            wL = shape.part(26).x
            hL = shape.part(22).y

        ROI_BGR_RIGHT  = imOrg[yR:hR,xR:wR]
        ROI_BGR_LEFT  = imOrg[yL:hL,xL:wL]
        ROI_GRAY = cv2.cvtColor(ROI_BGR_RIGHT,cv2.COLOR_BGR2GRAY)
        #cv2.imshow("TEST_GRAY",ROI_GRAY)
        #cv2.waitKey(0)

        im_bg = imOrg.copy()
        #---------------------------------------------------------------------------
        #ส่วนจัดการขนาดและ SMOOTH
        #---------------------------------------------------------------------------
        im_EyeBrown_Right = cv2.resize(im_EyeBrown_Right,(int(((wR-xR)+halfFace)),int(((hR-yR)+heightFace))))
        im_EyeBrown_LEFT = cv2.resize(im_EyeBrown_LEFT,(int(((wL-xL)+halfFace)),int(((hL-yL)+heightFace))))
        #im_EyeBrown_Right= cv2.GaussianBlur(im_EyeBrown_Right,(3,3),3)
        #im_EyeBrown_LEFT= cv2.GaussianBlur(im_EyeBrown_LEFT,(3,3),3)


        #---------------------------------------------------------------------------
        #CREAE MASK AND SEAMLESSCLONE
        mask_RIGHT = 255 * np.ones(im_EyeBrown_Right.shape, im_EyeBrown_Right.dtype)
        mask_LEFT = 255 * np.ones(im_EyeBrown_LEFT.shape, im_EyeBrown_LEFT.dtype)

        bg_width, bg_height, bg_channels = im_bg.shape
        point_RIGHT = (int((xR+wR)/2),int((yR+hR)/2))
        point_LEFT = (int((xL+wL)/2),int((yL+hL)/2))
        mixed_clone_RIGHT = cv2.seamlessClone(im_EyeBrown_Right, im_bg, mask_RIGHT,point_RIGHT, cv2.MIXED_CLONE)
        mixed_clone2_LEFT = cv2.seamlessClone(im_EyeBrown_LEFT, mixed_clone_RIGHT, mask_LEFT,point_LEFT, cv2.MIXED_CLONE)

        output_image = mixed_clone2_LEFT.copy()
        #mixed_clone_2 = cv2.seamlessClone(im_fg, imOrg, mask,point, cv2.MIXED_CLONE)
        #print ("XR = , YR  = ,WR = ,HR = ",xR,yR,wR,hR)
        #print ("HEIGHT,WIDTH = " ,output_image.shape[:2])

        UPLOAD_FOLDER = 'C:\\Users\\comsc\\AppData\\Local\\Programs\\Python\\Python36\\Project_senior\\tmp_images'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        #cv2.circle(output_image,point_RIGHT, 5, (0,255,0), -1)
        #cv2.circle(output_image,point_LEFT, 5, (0,255,0), -1)
        print("-----------------------------")
        #test = cv2.cvtColor(output_image,cv2.COLOR_BGR2RGB)
        #plt.imshow(output_image)
        #plt.show()
        #cv2.imshow("TEST",output_image)
        #cv2.waitKey(0)
        file_name = 'FILE_OUTPUT' + '__RESULT__' + '.jpg'
        path = os.path.join(UPLOAD_FOLDER,file_name)
        #output_image = cv2.cvtColor(output_image,cv2.COLOR_BGR2RGB)
        cv2.imwrite(path,output_image)
        
        return path
        