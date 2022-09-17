import cv2
import os


def handle_video():
    # os.system('sudo modprobe bcm2835-v4l2')
    cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
    cap.set(3,360)
    cap.set(4,240)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("No Devices found")
            break

        cv2.imshow('frame',frame)
        if cv2.waitKey(1)&0xff == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

handle_video()