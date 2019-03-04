from scipy import interpolate
from pylab import *
from skimage import color
import cv2
import dlib
from imutils import face_utils
import imutils
import numpy as np


Rg, Gg, Bg = (220., 91., 111.)
 # intensity of the blush
  # Approx x coordinate of center of the face.
'''
mid is used to construct the points for the blush in
the left cheek , as only the right cheek's points are
given as input.
'''

detector  = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

im = imread('input1.jpg')
#points = np.loadtxt('point1.txt')
#print(points)

height, width = im.shape[:2]
print(im.shape[:2])

gray_test = im[0,0,0]
intensity = (gray_test * 1.25) /1000
print(intensity)

imOrg = im.copy()
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
rects = detector(gray, 1)



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
cv2.circle(im,(int(x1),int(x2)),3,(0, 255, 0), -1)
cv2.circle(im,(y1,int(y2)),3,(255, 0, 0), -1)

cv2.circle(im,(w1,int(w2)),3,(255, 0, 255), -1)

cv2.circle(im,(int(h1),h2),3,(0, 0, 255), -1)

#cv2.circle(im,(464,522),3,(0, 0, 255), -1)

 
cv2.imshow("display",im)
cv2.waitKey(0)

def get_boundary_points(x, y):
    tck, u = interpolate.splprep([x, y], s=0, per=1)
    unew = np.linspace(u.min(), u.max(), 1000)
    xnew, ynew = interpolate.splev(unew, tck, der=0)
    tup = c_[xnew.astype(int), ynew.astype(int)].tolist()
    coord = list(set(tuple(map(tuple, tup))))
    coord = np.array([list(elem) for elem in coord])
    return np.array(coord[:, 0], dtype=np.int32), np.array(coord[:, 1], dtype=np.int32)


def apply_blush_color(r=Rg, g=Gg, b=Bg):
    global im
    val = color.rgb2lab((im / 255.)).reshape(width * height, 3)
    L, A, B = mean(val[:, 0]), mean(val[:, 1]), mean(val[:, 2])
    L1, A1, B1 = color.rgb2lab(np.array((r / 255., g / 255., b / 255.)).reshape(1, 1, 3)).reshape(3, )
    ll, aa, bb = (L1 - L) * intensity, (A1 - A) * intensity, (B1 - B) * intensity
    val[:, 0] = np.clip(val[:, 0] + ll, 0, 100)
    val[:, 1] = np.clip(val[:, 1] + aa, -127, 128)
    val[:, 2] = np.clip(val[:, 2] + bb, -127, 128)
    im = color.lab2rgb(val.reshape(height, width, 3)) * 255


def smoothen_blush(x, y):
    global imOrg
    imgBase = zeros((height, width))
    cv2.fillConvexPoly(imgBase, np.array(c_[x, y], dtype='int32'), 1)
    imgMask = cv2.GaussianBlur(imgBase, (51, 51), 0)
    imgBlur3D = np.ndarray([height, width, 3], dtype='float')
    imgBlur3D[:, :, 0] = imgMask
    imgBlur3D[:, :, 1] = imgMask
    imgBlur3D[:, :, 2] = imgMask
    imOrg = (imgBlur3D * im + (1 - imgBlur3D) * imOrg).astype('uint8')


x, y = points[0:5, 0], points[0:5, 1]
x, y = get_boundary_points(x, y)
apply_blush_color()
smoothen_blush(x, y)
smoothen_blush(2 * mid * ones(len(x)) - x, y)

figure()
print("TEST")
print(imOrg.shape[0:2])
#cv2.imshow("DISPLAY",imOrg)
plt.imshow(imOrg)
cv2.waitKey(0)

imsave('output.jpg', imOrg)
show()