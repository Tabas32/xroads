from imageai.Detection.Custom import CustomObjectDetection
from videoDetector import getObjects, markObjectsCV
import cv2
import numpy as np

def setUpNN(model_path, json_path):
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(model_path)
    detector.setJsonPath(json_path)
    detector.loadModel()

    return detector

def detect(detector, input):
    return detector.detectObjectsFromImage(input_image=input, input_type="array", output_type="array",
                                            extract_detected_objects=False, minimum_percentage_probability=30, nms_treshold=0.2,
                                            display_percentage_probability=True, display_object_name=False)

def liveShow(camera, model_path, json_path, object_name):
    cap = cv2.VideoCapture(camera)

    detector = setUpNN(model_path, json_path)
    while(True):
        ret, frame = cap.read()

        output_img, detections = detect(detector, np.asarray(frame), model_path)
        all_objs = getObjects(detections, object_name)
        cv2.imshow("img", markObjectsCV(frame, all_objs))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

"""
    How to use:
        from customVideoDetector import liveShow
        
        model_path  = "PATH_TO_MODEL.h5"
        json_path   = "PATH_TO_JSON.json"

        liveShow(0, model_path, json_path, 'ozobot')
"""
