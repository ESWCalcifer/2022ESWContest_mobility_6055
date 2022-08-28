# Programme core
from id_distance import calc_all_distance
import pickle
from data_generate import num_hand
import hand_detection_module
import cv2
model_name = 'hand_model.sav'

# custom function
def rps(num):
    if num == 0:
        return 'PAPER'
    elif num == 1:
        return 'GOOD'
    else:
        return 'SCISSOR'

font = cv2.FONT_HERSHEY_PLAIN
hands = hand_detection_module.HandDetector(max_hands=num_hand)
model = pickle.load(open(model_name, 'rb'))

cap_laptop = cv2.VideoCapture(cv2.CAP_DSHOW)
cap_usb= cv2.VideoCapture(cv2.CAP_DSHOW+1)


while cap_laptop.isOpened():
    success_laptop, frame_laptop = cap_laptop.read()
    if not success_laptop:
        print("Ignoring empty camera frame.")
        continue
    # image, my_list = hands.find_hand_landmarks(cv2.flip(frame_usb, 1), draw_landmarks=False)

    if my_list:
        height, width, _ = image.shape
        all_distance = calc_all_distance(height, width, my_list)
        pred = rps(model.predict([all_distance])[0])
        pos = (int(my_list[12][0]*height), int(my_list[12][1]*width))
        image = cv2.putText(image, pred, pos, font, 2, (0, 0, 0), 2)
        if pred == "SCISSOR":
            index = 0
            while cap_usb.isOpened():
                success_usb, frame_usb = cap_usb.read()
                if success_usb:
                    index += 1
                    cv2.imwrite(str(index) + '.png', frame_laptop)
                else:
                    break
            # cap_laptop.release()

    cv2.imshow('Hands', image)
    cv2.waitKey(1)
