from pylab import *
from scipy.interpolate import interp1d
from skimage import color
import cv2
import dlib
import os

class LipMakeup_class():
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.Rg = 0
        self.Gg = 0
        self.Bg = 0

    def inter(self,lx, ly, k1='quadratic'):
        unew = np.arange(lx[0], lx[-1] + 1, 1)
        f2 = interp1d(lx, ly, kind=k1)
        return f2, unew


    def ext(self,a, b, i):
        a, b = np.round(a), np.round(b)
        self.x.extend(arange(a, b, 1, dtype=np.int32).tolist())
        self.y.extend((ones(int(b - a), dtype=np.int32) * i).tolist())


    def apply_lipstick_func(self,imageFile,r,g,b):

        detector  = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

        self.Rg = r
        self.Gg = g
        self.Bg = b

        up_left_end = 3
        up_right_end = 5
        
        figure()
        im = cv2.imread(imageFile)
        imOrg = im.copy()
        
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
            mid = shape.part(33).x 

            x49 = shape.part(48).x
            y49 = shape.part(48).y

            x51 = shape.part(50).x
            y51 = shape.part(50).y

            x52 = shape.part(51).x
            y52 = shape.part(51).y

            x53 = shape.part(52).x
            y53 = shape.part(52).y

            x55 = shape.part(54).x
            y55 = shape.part(54).y

            x57 = shape.part(56).x
            y57 = shape.part(56).y

            x59 = shape.part(58).x
            y59 = shape.part(58).y

            x61 = shape.part(60).x
            y61 = shape.part(60).y

            x62 = shape.part(61).x
            y62 = shape.part(61).y

            x63 = shape.part(62).x
            y63 = shape.part(62).y

            x64 = shape.part(63).x
            y64 = shape.part(63).y

            x65 = shape.part(64).x
            y65 = shape.part(64).y

            x66 = shape.part(65).x
            y66 = shape.part(65).y

            x68 = shape.part(67).x
            y68 = shape.part(67).y

    
            points = np.array([[x49,y49],[x51,y51],[x52,y52],[x53,y53],[x55,y55],[x57,y57],[x59,y59]
            ,[x61,y61],[x62,y62],[x63,y63],[x64,y64],[x65,y65],[x66,y66],[x68,y68]])

        # gets the points on the boundary of lips from the file
        #file = np.loadtxt('pointpixel.txt')
        points = np.floor(points)
        point_out_x = np.array((points[:len(points) // 2][:, 0]))
        point_out_y = np.array(points[:len(points) // 2][:, 1])
        point_in_x = (points[len(points) // 2:][:, 0])
        point_in_y = points[len(points) // 2:][:, 1]

        
        # Code for the curves bounding the lips
        o_u_l = self.inter(point_out_x[:up_left_end], point_out_y[:up_left_end])
        o_u_r = self.inter(point_out_x[up_left_end - 1:up_right_end], point_out_y[up_left_end - 1:up_right_end])
        o_l = self.inter([point_out_x[0]] + point_out_x[up_right_end - 1:][::-1].tolist(),
                [point_out_y[0]] + point_out_y[up_right_end - 1:][::-1].tolist(), 'cubic')
        i_u_l = self.inter(point_in_x[:up_left_end], point_in_y[:up_left_end])
        i_u_r = self.inter(point_in_x[up_left_end - 1:up_right_end], point_in_y[up_left_end - 1:up_right_end])
        i_l = self.inter([point_in_x[0]] + point_in_x[up_right_end - 1:][::-1].tolist(),
                    [point_in_y[0]] + point_in_y[up_right_end - 1:][::-1].tolist(), 'cubic')

        self.x = []  # will contain the x coordinates of points on lips
        self.y = []  # will contain the y coordinates of points on lips



        for i in range(int(o_u_l[1][0]), int(i_u_l[1][0] + 1)):
            self.ext(o_u_l[0](i), o_l[0](i) + 1, i)

        for i in range(int(i_u_l[1][0]), int(o_u_l[1][-1] + 1)):
            self.ext(o_u_l[0](i), i_u_l[0](i) + 1, i)
            self.ext(i_l[0](i), o_l[0](i) + 1, i)

        for i in range(int(i_u_r[1][-1]), int(o_u_r[1][-1] + 1)):
            self.ext(o_u_r[0](i), o_l[0](i) + 1, i)

        for i in range(int(i_u_r[1][0]), int(i_u_r[1][-1] + 1)):
            self.ext(o_u_r[0](i), i_u_r[0](i) + 1, i)
            self.ext(i_l[0](i), o_l[0](i) + 1, i)

        # Now x and y contains coordinates of all the points on lips

        val = color.rgb2lab((imOrg[self.x, self.y] / 255.).reshape(len(self.x), 1, 3)).reshape(len(self.x), 3)
        L, A, B = mean(val[:, 0]), mean(val[:, 1]), mean(val[:, 2])
        L1, A1, B1 = color.rgb2lab(np.array((r / 255., g / 255., b / 255.)).reshape(1, 1, 3)).reshape(3, )
        ll, aa, bb = L1 - L, A1 - A, B1 - B
        val[:, 0] += ll
        val[:, 1] += aa
        val[:, 2] += bb

        imOrg[self.x, self.y] = color.lab2rgb(val.reshape(len(self.x), 1, 3)).reshape(len(self.x), 3) * 255
        gca().set_aspect('equal', adjustable='box')
        #imshow(imOrg)
        #show()
        #imsave('output.jpg', im)
        UPLOAD_FOLDER = 'C:\\Users\\comsc\\AppData\\Local\\Programs\\Python\\Python36\\Project_senior\\tmp_images'
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
        name = 'apply_lipstick'
        file_name = 'output_' + name + '.jpg'
        path = os.path.join(UPLOAD_FOLDER,file_name)
        imOrg = cv2.cvtColor(imOrg,cv2.COLOR_BGR2RGB)
        cv2.imwrite(path,imOrg)
        return file_name