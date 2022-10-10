import cv2
import time
import sys
import numpy as np
from openvino.inference_engine import IECore
import sqlite3

INPUT_WIDTH = 256
INPUT_HEIGHT = 256
SCORE_THRESHOLD = 0.2
NMS_THRESHOLD = 0.4
CONFIDENCE_THRESHOLD = 0.4

colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]


start = time.time_ns()
frame_count = 0
total_frames = 0
fps = -1

class_name = ["ANIMAL", "PERSON", "VEHICLE"]
con = sqlite3.connect("video_db", check_same_thread=False)
cur = con.cursor()
class video_detection():
    def __init__(self):
        ie_core = IECore()
        converted_model_path = "./md_v5a.0.0.xml" #구글 드라이브에서 뒤에 openvino 있는 7z 파일 받아서 쓰세요
        network = ie_core.read_network(model=converted_model_path)
        self.exec_net_ir = ie_core.load_network(network=network, device_name="MYRIAD")
        self.input_layer_ir = next(iter(self.exec_net_ir.input_info))
        self.output_layer_ir = next(iter(self.exec_net_ir.outputs))
        self.capture = cv2.VideoCapture(0)


    def detect(self, image):
        blob = cv2.dnn.blobFromImage(
            image, 1/255.0, (INPUT_WIDTH, INPUT_HEIGHT), swapRB=True, crop=False)
        preds = self.exec_net_ir.infer(inputs={self.input_layer_ir: blob})
        preds = preds[self.output_layer_ir]
        return preds

    def wrap_detection(self, input_image, output_data):
        class_ids = []
        confidences = []
        boxes = []
        rows = output_data.shape[0]
        image_width, image_height, _ = input_image.shape
        x_factor = image_width / INPUT_WIDTH
        y_factor = image_height / INPUT_HEIGHT
        for r in range(rows):
            row = output_data[r]
            confidence = row[4]
            if confidence >= 0.4:
                classes_scores = row[5:]
                _, _, _, max_indx = cv2.minMaxLoc(classes_scores)
                class_id = max_indx[1]
                if (classes_scores[class_id] > .25):
                    confidences.append(float(confidence))
                    class_ids.append(class_id)
                    x, y, w, h = row[0].item(), row[1].item(
                    ), row[2].item(), row[3].item()
                    left = int((x - 0.5 * w) * x_factor)
                    top = int((y - 0.5 * h) * y_factor)
                    width = int(w * x_factor)
                    height = int(h * y_factor)
                    box = np.array([left, top, width, height])
                    boxes.append(box)
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)
        indexes = np.array(indexes)
        result_class_ids = []
        result_confidences = []
        result_boxes = []
        for i in indexes:
            result_confidences.append(confidences[i])
            result_class_ids.append(class_ids[i])
            result_boxes.append(boxes[i])
        if len(result_boxes) > 0:
            cur.execute("update video set detected='True' where camera_id=0")
            con.commit()
        else:
            cur.execute("update video set detected='False' where camera_id=0")
            con.commit()
        return result_class_ids, result_confidences, result_boxes

    def format_yolov5(self, frame):
        row, col, _ = frame.shape
        _max = max(col, row)
        result = np.zeros((_max, _max, 3), np.uint8)
        result[0:row, 0:col] = frame
        return result
    def get_frame(self):
        _, frame = self.capture.read()
        inputImage = self.format_yolov5(frame)
        outs = self.detect(inputImage)
        class_ids, confidences, boxes = self.wrap_detection(inputImage, outs[0])
        for (classid, confidence, box) in zip(class_ids, confidences, boxes):
            color = colors[int(classid) % len(colors)]
            cv2.rectangle(frame, box, color, 2)
            cv2.rectangle(frame, (box[0], box[1] - 20),
                        (box[0] + box[2], box[1]), color, -1)
            cv2.putText(frame, class_name[classid], (box[0],
                                                box[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0))
        return frame

