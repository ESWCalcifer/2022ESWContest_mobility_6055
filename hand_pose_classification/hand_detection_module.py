import cv2
import mediapipe as mp

class HandDetector:
  def __init__(self,
               mode=False, max_hands=2,
               min_detection_confidence=0.5, min_tracking_confidence=0.5):
    self.mode = mode
    self.max_hands = max_hands
    self.dict_confidence  = min_detection_confidence
    self.track_confidence = min_tracking_confidence

    self.mp_hands = mp.solutions.hands
    self.hands = self.mp_hands.Hands(static_image_mode= mode,
                                     max_num_hands = max_hands,
                                     min_detection_confidence= min_detection_confidence,
                                     min_tracking_confidence= min_tracking_confidence)
    self.mp_drawing = mp.solutions.drawing_utils

  def find_hand_landmarks(self, image, draw_landmarks=False):
    landmark_list = []
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img.flags.writeable = False
    results = self.hands.process(img)
    img.flags.writeable = True
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        if draw_landmarks:
          self.mp_drawing.draw_landmarks(img, hand_landmarks
                                         , self.mp_hands.HAND_CONNECTIONS)
        for i in range(21):
          per_point = [hand_landmarks.landmark[i].x,
                       hand_landmarks.landmark[i].y,
                       hand_landmarks.landmark[i].z]
          landmark_list.append(per_point)
    return img, landmark_list

