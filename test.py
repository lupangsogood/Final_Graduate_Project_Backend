from LipsEyeliner_Makeup import ApplyMakeup
from Brush_Makeup.blush import Brush_Makeup
import cv2
import os

path_image = 'Project_senior\Input3.jpg'
print(path_image)
AM = ApplyMakeup()


output_file = AM.apply_lipstick(path_image,195,0,30) 
output_file2 =AM.apply_liner(output_file)

output3 = Brush_Makeup(output_file2)

#output_file2 = AM.apply_liner('C:\\Users\\ANUSIT\\Desktop\\detect-face-parts\\input.jpg')


 