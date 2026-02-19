import cv2
import pygame

w = 800
h = 600
dbg_lm_txt_col = (255,0,0)
dbg_lm_lines_col = (0,255,0)
dbg_line_thickness = 1
dbg_txt_thickness = 1
dbg_txt_scale = 0.5
my_font = cv2.FONT_HERSHEY_SIMPLEX
zoom_func = lambda x: 5+ x*10
trans_func = lambda t: t*40
rot_func = lambda r: r*10
