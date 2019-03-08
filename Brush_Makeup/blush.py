from scipy import interpolate
from pylab import *
from skimage import color
import cv2
import dlib
from imutils import face_utils
import imutils
import numpy as np


class BrushMakeup_class():

    def __init__(self):
        self.im = 0
        self.imOrg = 0
        self.Rg = 0
        self.Gg = 0
        self.Bg = 0
        self.height = 0
        self.width = 0
        self.intensity = 0
        


    def get_boundary_points(self,x, y):
        tck, u = interpolate.splprep([x, y], s=0, per=1)
        unew = np.linspace(u.min(), u.max(), 1000)
        xnew, ynew = interpolate.splev(unew, tck, der=0)
        tup = c_[xnew.astype(int), ynew.astype(int)].tolist()
        coord = list(set(tuple(map(tuple, tup))))
        coord = np.array([list(elem) for elem in coord])
        return np.array(coord[:, 0], dtype=np.int32), np.array(coord[:, 1], dtype=np.int32)


    def apply_blush_color(self):
        r = self.Rg
        g = self.Gg
        b = self.Bg
        print(r,g,b)
        val = color.rgb2lab((self.im / 255.)).reshape(self.width * self.height, 3)
        L, A, B = mean(val[:, 0]), mean(val[:, 1]), mean(val[:, 2])
        L1, A1, B1 = color.rgb2lab(np.array((r / 255., g / 255., b / 255.)).reshape(1, 1, 3)).reshape(3, )
        ll, aa, bb = (L1 - L) * self.intensity, (A1 - A) * self.intensity, (B1 - B) * self.intensity
        val[:, 0] = np.clip(val[:, 0] + ll, 0, 100)
        val[:, 1] = np.clip(val[:, 1] + aa, -127, 128)
        val[:, 2] = np.clip(val[:, 2] + bb, -127, 128)
        self.im = color.lab2rgb(val.reshape(self.height, self.width, 3)) * 255


    def smoothen_blush(self,x, y):
        global imOrg
        imgBase = zeros((self.height, self.width))
        cv2.fillConvexPoly(imgBase, np.array(c_[x, y], dtype='int32'), 1)
        imgMask = cv2.GaussianBlur(imgBase, (51, 51), 0)
        imgBlur3D = np.ndarray([self.height, self.width, 3], dtype='float')
        imgBlur3D[:, :, 0] = imgMask
        imgBlur3D[:, :, 1] = imgMask
        imgBlur3D[:, :, 2] = imgMask
        self.imOrg = (imgBlur3D * self.im + (1 - imgBlur3D) * self.imOrg).astype('uint8')



    def apply_brush(self,imageFile,r,g,b):
        
        self.Rg = r 
        self.Gg = g
        self.Bg = b
        
        detector  = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        self.im = imread(imageFile)
        #points = np.loadtxt('point1.txt')
        #print(points)

        self.height, self.width = self.im.shape[:2]
        print(self.im.shape[:2])



        self.imOrg = self.im.copy()
        imRoi = self.im.copy()
        gray = cv2.cvtColor(self.im, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)


        ####FOR LOOP CHEEK_POSITION####
        for (i,rect) in enumerate(rects):
            shape = predictor(gray,rect)

            #ค่าความกว้างของหน้า และ ความสูงของหน้า
            HALF_FACE_RATIO = (0.695)
            halfFace = shape.part(16).x * HALF_FACE_RATIO
            FACE_HEIGHT_RATIO = (1.0 / 5)
            heightFace = shape.part(8).y * FACE_HEIGHT_RATIO

            #ค่าจุดกลางของหน้าเอาไว้จุดแก้มอีกหนึ่งข้าง
            mid = shape.part(33).x 


            x1 = (shape.part(35).x+int(halfFace))/1.7
            x2 = shape.part(28).y+(heightFace/3.5)

            y1 = shape.part(13).x
            y2 = shape.part(28).y+(heightFace/3.5)

            w1 = shape.part(13).x
            w2 = shape.part(14).y+(heightFace/5)

            h1 =(shape.part(35).x+int(halfFace))/1.7
            h2 =shape.part(35).y


            ROI = imRoi[int(shape.part(28).y):int(h2+(x2/5)),int(shape.part(37).x):int(w1)]

    
            gray_test = ROI[0,0,0]
            gray_test_2 = self.im[0,0,0]
            intensity2 = (gray_test_2*1.5)/1000
            self.intensity = (gray_test*1.5)/1000
            print(self.intensity)

            cv2.imshow("ROI",ROI)
            cv2.waitKey(0)


            #print(x2,y2,w2,h2)
            #print(shape.part(0).x,shape.part(16).x)
            print(halfFace)
            print(heightFace)
            print(x1,x2)
            print(y1,y2)
            print(w1,w2)
            print(h1,h2)

            points = np.array([[x1,x2],[y1,y2],[w1,w2],[h1,h2]])

            #cv2.circle(im,(int(x2),int(test)),3,(0, 255, 0), -1)
            cv2.circle(self.im,(int(x1),int(x2)),3,(0, 255, 0), -1)
            cv2.circle(self.im,(y1,int(y2)),3,(255, 0, 0), -1)

            cv2.circle(self.im,(w1,int(w2)),3,(255, 0, 255), -1)

            cv2.circle(self.im,(int(h1),h2),3,(0, 0, 255), -1)

            #cv2.circle(im,(464,522),3,(0, 0, 255), -1)


            cv2.imshow("display",self.im)
            cv2.waitKey(0)

        x, y = points[0:5, 0], points[0:5, 1]
        x, y = self.get_boundary_points(x, y)
        self.apply_blush_color()
        self.smoothen_blush(x, y)
        self.smoothen_blush(2 * mid * ones(len(x)) - x, y)

        figure()
        print("TEST_imOrg")
        print(self.imOrg.shape[0:2])
        #cv2.imshow("DISPLAY",imOrg)
        plt.imshow(self.imOrg)
        cv2.waitKey(0)

        imsave('output.jpg', self.imOrg)
        show()
