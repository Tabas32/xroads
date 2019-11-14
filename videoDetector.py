from imageai.Detection import ObjectDetection
from PIL import Image
import cv2

def setUpNN(model_path):
    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    return detector

def detect(detector, input):
    return detector.detectObjectsFromImage(input_image = input,
                                           input_type = "array",
                                           output_type = "array")

def getObjects(detections, object_name):
    all_objects = []
    for eachObject in detections:
        if eachObject["name"] == object_name:
            item = {"bp" : eachObject["box_points"],
                    "prob" : eachObject["percentage_probability"]}
            all_objects.append(item)


    return all_objects


def markObjects(image_path, objects_boxes):
    im = Image.open(image_path)
    imW, imH = im.size
    imgout = cv2.imread(image_path, cv2.IMREAD_COLOR)
    for obj in objects_boxes:
       cv2.circle(imgout,(int((obj[0]+obj[2])/2), int((obj[1]+obj[3])/2)), 25, (0,0,255), -1)

    return imgout

def markObjectsCV(image, objects):
    for obj in objects:
       cv2.circle(image,(int((obj["bp"][0]+obj["bp"][2])/2), int((obj["bp"][1]+obj["bp"][3])/2)), 18, (0,0,255), -1)

    return image

"""
model_path  = "./models/yolo-tiny.h5"

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 160)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 120)

detector = setUpNN(model_path)
while(True):
    ret, frame = cap.read()

    output_img, detections = detect(detector, np.asarray(frame), model_path)
    all_objs = getObjectBoxes(detections, 'bottle')
    cv2.imshow("img", markObjectsCV(frame, all_objs))

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
"""
