from Lips_Eyeliner_Makeup.apply_makeup import ApplyMakeup
from Brush_Makeup.blush import BrushMakeup_class
from Lip_Makeup.lipstick import LipMakeup_class
from Eyebrown_Makeup.eyebrown import Eyebrown_Makeup_class
import cv2

#------------------------- CHECK PATH AFTER GIT PULL ----------------------------------#
#-----------------------FOR NOTE_BOOK --------------------------------------------------#
'''
path_image = 'C:\\Users\\ANUSIT\\Anaconda3\\envs\\opencv-env\\Project_senior\\Project_senior\\images_input\\input14.jpg'
print(path_image)
path_eyebrown_R = 'C:\\Users\\ANUSIT\\Anaconda3\\envs\\opencv-env\\Project_senior\\Project_senior\\drawable\\testjangmakR1.jpg'
path_eyebrown_L = 'C:\\Users\\ANUSIT\\Anaconda3\\envs\\opencv-env\\Project_senior\\Project_senior\\drawable\\testjangmakL1.jpg'
'''
#----------------------------------FOR COMPUTER ----------------------------------------#
path_image = 'C:\\Users\\ANUSIT\\Documents\\GitHub\\Project_senior\\images_intput\\input14.jpg'
print(path_image)
path_eyebrown_R = 'C:\\Users\ANUSIT\\Documents\\GitHub\\Project_senior\\drawable\\testjangmakR1.jpg'
path_eyebrown_L = 'C:\\Users\ANUSIT\\Documents\\GitHub\\Project_senior\\drawable\\testjangmakL1.jpg'


AM = ApplyMakeup()
BM = BrushMakeup_class()
LM = LipMakeup_class()
EM = Eyebrown_Makeup_class()

output_file1 = AM.apply_liner(path_image)
output_file2 = BM.apply_brush(output_file1,192,131,114)
output_file3 = LM.apply_lipstick_func(output_file2,175,66,68)
output_file4 = EM.apply_Eyebrown(output_file3,path_eyebrown_R,path_eyebrown_L)
