from LipsEyeliner_Makeup import ApplyMakeup
from Brush_Makeup.blush import BrushMakeup_class
from Lip_Makeup.lipstick import LipMakeup_class
import cv2
import os

path_image = 'Project_senior\input1.jpg'
print(path_image)
AM = ApplyMakeup()
BM = BrushMakeup_class()
LM = LipMakeup_class()



output_file1 = AM.apply_liner(path_image)
output_file2 = BM.apply_brush(output_file1,204,40,57)
output_file3 = LM.apply_lipstick_func(output_file2,207,40,57)
