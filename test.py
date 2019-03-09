from LipsEyeliner_Makeup import ApplyMakeup
from Brush_Makeup.blush import BrushMakeup_class
from Lip_Makeup.lipstick import LipMakeup_class
import cv2
import os

path_image = 'Project_senior\input3.jpg'
print(path_image)
AM = ApplyMakeup()
BM = BrushMakeup_class()
LM = LipMakeup_class()


output_file = LM.apply_lipstick_func(path_image,255,0,0)
#output_file2 =AM.apply_liner(output_file)

#test = BM.apply_brush(output_file2,255,0,255)

