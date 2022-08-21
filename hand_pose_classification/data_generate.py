# Programme core
num_hand = 1
num_class = 3
num_instance = 500 #per_class
break_time = 1 #min 2 seconds

# uga buga functions

if __name__ == '__main__':
    import cv2
    import pandas as pd
    import time
    import hand_detection_module
    from id_distance import calc_all_distance


    full_data = []
    data_target = 0

    hands = hand_detection_module.HandDetector(max_hands=num_hand)
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue
        image, my_list = hands.find_hand_landmarks(cv2.flip(frame, 1),
                                                   draw_landmarks=True)
        if my_list:
            height, width, _ = image.shape
            distance_list = calc_all_distance(height, width, my_list)
            full_data.append(distance_list)
            print(len(full_data))
        cv2.imshow('Hands', image)
        cv2.waitKey(1)
        if len(full_data) >= num_instance:
            print('Creating Pandas DataFrame...')
            hand1_df = pd.DataFrame(full_data)
            hand1_df['y'] = data_target
            hand1_df.to_csv(f'hand-{data_target}.csv', index=False)
            data_target +=1
            full_data = []
            if data_target >= num_class: break
            else:
                time.sleep(break_time)
                print('1 sec left at the time_sleep ....')
                time.sleep(1)

    cap.release()
