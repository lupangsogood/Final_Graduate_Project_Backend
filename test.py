from LipsEyeliner_Makeup import ApplyMakeup
from Brush_Makeup.blush import BrushMakeup_class
import cv2
import os

path_image = 'Project_senior\Input3.jpg'
print(path_image)
AM = ApplyMakeup()
BM = BrushMakeup_class()


output_file = AM.apply_lipstick(path_image,195,0,0 ) 
output_file2 =AM.apply_liner(output_file)

test = BM.apply_brush(output_file2,255,0,255)

