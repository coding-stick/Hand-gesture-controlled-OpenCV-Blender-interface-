import math, cv2
from config import *
import numpy as np

def get_angle_2lines(line1: list|tuple, line2: list|tuple):
    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    # Calculate direction vectors
    v1 = (x2 - x1, y2 - y1)
    v2 = (x4 - x3, y4 - y3)

    angle1 = math.atan2(v1[1], v1[0])
    angle2 = math.atan2(v2[1], v2[0])

    # Calculate signed angle difference in degrees
    angle_degrees = math.degrees(angle2 - angle1)
    angle_degrees%=180
    if angle_degrees<0: angle_degrees +=360
    if angle_degrees > 360: angle_degrees=360-angle_degrees
    return angle_degrees



def get_angle_vector_w_horiz(vec:np.ndarray) -> float:
    return math.atan2(vec[1], vec[0])

def to_screen(p:np.ndarray, w=w, h=h):
    sx = int(p[0] * w)
    sy = int(p[1] * h)
    return (sx, sy)


def angles_bween_2vectors(vec1:np.ndarray, vec2:np.ndarray):
    unit_vec1 = vec1 / np.linalg.norm(vec1)
    unit_vec2 = vec2 / np.linalg.norm(vec2)
    dot_product = np.dot(unit_vec1, unit_vec2)
    angle_radians = np.arccos(dot_product)
    angle_degrees = np.degrees(angle_radians)
    return angle_radians, angle_degrees

def landmarks_list_to_pos_arrays(landmarks) -> np.ndarray:
    for i in range(0,20):
        return np.array([np.array([lm.x, lm.y, lm.z]) for lm in landmarks])

def manual_dist(p1:np.ndarray, p2:np.ndarray, scale=1) -> float:
    return np.linalg.norm(p1 - p2)*scale



def angle_with_horizontal(line1, line2):
    (x1, y1) = line1
    (x2, y2) = line2
    dx = x1=x2
    dy = y1-y2

    angle_radians = math.atan2(dy, dx)  # atan2 handles the quadrant correctly
    angle_degrees = math.degrees(angle_radians)
    return angle_degrees

def find_midpoint_bween_2vectors(p1:np.ndarray,p2:np.ndarray, round_n = True):
    mx = (p1[0] + p2[0]) / 2
    my = (p1[1] + p2[1]) / 2
    mz = (p1[2] + p2[2]) / 2
    if round_n:
        return np.array([round(mx), round(my), round(mz)])
    return np.array([mx, my, mz])

def default_line(frame, p1,p2):
    cv2.line(frame, p1, p2, dbg_lm_lines_col, dbg_line_thickness)

def default_text(frame, text, pos):
    cv2.putText(frame, text, pos, my_font, dbg_txt_scale, dbg_lm_txt_col, dbg_txt_thickness)