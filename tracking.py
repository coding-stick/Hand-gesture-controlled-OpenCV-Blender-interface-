import cv2
import mediapipe as mp
import threading
import math
from funcs import *
from config import *


mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)


rotation_mode = 'off'
starting_TI_line =None
right_mid = None
left_mid = None
starting_mid_mid = None

class HandTracker:
    def __init__(self):
        self.zoom = 0
        self.rotation = np.array([0,0,0])
        self.translate = np.array([0,0,0])


    def stop(self):
        self._stop = True
        self.thread.join()

    def run(self):
        global rotation_mode, starting_TI_line, right_mid, left_mid, starting_mid_mid, starting_length_2hands


        success, frame = cap.read()

        if not success:
            print("Failed to capture video")
            return

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        h, w, _ = frame.shape


        if result.multi_hand_landmarks and result.multi_handedness:
            
            if len(result.multi_hand_landmarks)==2:
                # 2 hands


                for i, hand_landmarks in enumerate(result.multi_hand_landmarks):

                    hand_label = result.multi_handedness[i].classification[0].label
                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


                    all_lm_pos = landmarks_list_to_pos_arrays(hand_landmarks.landmark)
                    for i, pos in enumerate(all_lm_pos):
                        # draw write the index of the landmark next to it on the screen
                        cx, cy = to_screen(pos, w, h)
                        default_text(frame, str(i), (cx+10, cy+10))
                    
                    

                    thumb = all_lm_pos[4]
                    index = all_lm_pos[8]

                    dist_thumb_index = manual_dist(thumb, index)

                    default_line(frame, to_screen(thumb, w, h), to_screen(index, w, h))

                    if hand_label == "Right":
                        right_mid = find_midpoint_bween_2vectors(thumb, index, round_n=False)
                        default_text(frame, f'index-thumb dist: {round(dist_thumb_index, 4)}', (10,60))
                    if hand_label == "Left":
                        left_mid = find_midpoint_bween_2vectors(thumb, index, round_n=False)

                    if right_mid is not None and left_mid is not None:
                        default_line(frame, to_screen(right_mid, w, h), to_screen(left_mid, w, h))
                        if dist_thumb_index <= 0.1:
                            starting_length_2hands = math.dist(left_mid, right_mid)
                            
                            starting_mid_mid = find_midpoint_bween_2vectors(right_mid, left_mid)
                            self.translate = np.array([0,0,0])
                            self.zoom = 0

                            
                        else:
                            current_length_2hands = math.dist(left_mid, right_mid)
                            current_mid_mid = find_midpoint_bween_2vectors(right_mid, left_mid, round_n=False)
                            if starting_mid_mid is not None:
                                translation = current_mid_mid - starting_mid_mid
                                scale = current_length_2hands - starting_length_2hands

                                self.zoom = scale
                                self.translate= translation
                                default_text(frame, f'translation: {translation}, zoom: {scale}', (10,90))

            else:
                self.zoom = 0
                self.translate = np.array([0,0,0])

                for i, hand_landmarks in enumerate(result.multi_hand_landmarks):

                    mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    #print(hand_landmarks.landmark)
                    all_lm_pos = landmarks_list_to_pos_arrays(hand_landmarks.landmark)

                    thumb = all_lm_pos[4]
                    index = all_lm_pos[8]
                    pinky = all_lm_pos[20]
                    origin = all_lm_pos[0]

                    posT = to_screen(thumb, w, h)
                    posI = to_screen(index, w, h)
                    posP = to_screen(pinky, w, h)
                    pos0 = to_screen(origin, w, h)

                    thumb_index_dist = manual_dist(thumb, index)
                    pinky_origin_dist = manual_dist(pinky, origin)

                    current_TI_line = thumb - index

                    index_angle = get_angle_vector_w_horiz(current_TI_line)
                    if thumb_index_dist <= 0.1:
                        rotation_mode = 'off'
                        #self.state['rotation'] = 0
                        starting_TI_line = thumb - index
                    elif thumb_index_dist > 0.1 and pinky_origin_dist <=0.2:
                        rotation_mode = 'auto'
                        self.rotation = self.rotation.astype(float)
                        self.rotation += 0.01
                    elif thumb_index_dist > 0.1 and pinky_origin_dist > 0.3:
                        rotation_mode = 'manual'
                        if starting_TI_line is not None:
                            #print(starting_line)
                            current_rotation = angles_bween_2vectors(starting_TI_line, current_TI_line)[1]
                            disp = starting_TI_line - current_TI_line
                            self.rotation = disp
                            default_text(frame, f'I-T displacement w: {disp}', (10,10))
                            
                    
                    default_line(frame, posT, posI)
                    default_line(frame, posP, pos0)
                    
                    
                    default_text(frame, f'index angle w/ horizontal: {int(math.degrees(index_angle))}', (10,30))
                    default_text(frame, f'index-thumb dist: {round(thumb_index_dist, 4)}, rotation:{rotation_mode}', (10,50))
                    default_text(frame, f'pinky-origin dist: {round(pinky_origin_dist, 4)}', (10,70))


        #print(self.rotation, self.translate, self.zoom)
        cv2.imshow("Hand Tracking", frame)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()



