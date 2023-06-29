from django.shortcuts import render
from django.urls import reverse_lazy
from stream_control.models import DetectedImage
from django.shortcuts import redirect
from django.http import HttpResponse
from playsound import playsound
from django.conf import settings
from blynkapi import Blynk
import blynklib
import requests

def detect(request):
    return render(request,"stream_control/detect.html")

def gotodetect(request):
    return render(request,"stream_control/detect.html")

def detect_person(request):
    import cv2
    import pytesseract
    import numpy as np
    import time
    import pyttsx3
    import os
    from gtts import gTTS
    from playsound import playsound

    net = cv2.dnn.readNet("stream_control/yolov3.weights", "stream_control/yolov3.cfg")

    with open("stream_control/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]

    frames_since_last_detection = {}
    previous_detected_objects=[]

    output_layers = net.getUnconnectedOutLayersNames()
    detected_objects = set()

    engine = pyttsx3.init()

    cap = cv2.VideoCapture(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    def post_process(frame, outputs, conf_threshold, nms_threshold):
        height, width, _ = frame.shape
        boxes = []
        confidences = []
        class_ids = []
    
        for output in outputs:
            for detection in output:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > conf_threshold:
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)
                    x = center_x - w // 2
                    y = center_y - h // 2
                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
    
        return [boxes[i] for i in indices], [confidences[i] for i in indices], [class_ids[i] for i in indices]

    while True:
        ret, frame = cap.read()
        conf_threshold = 0.5  # Confidence threshold for filtering out weak detections
        nms_threshold = 0.4   # Non-maximum suppression threshold for eliminating overlapping boxes

        # Detect objects in the frame
        blob = cv2.dnn.blobFromImage(frame, 1/255, (416, 416), swapRB=True)
        net.setInput(blob)
        outputs = net.forward(output_layers)
        boxes, confidences, class_ids = post_process(frame, outputs, conf_threshold, nms_threshold)

        # Update frames_since_last_detection
        for i in range(len(frames_since_last_detection)):
            object_name = list(frames_since_last_detection.keys())[i]
            if object_name in detected_objects:
                frames_since_last_detection[object_name] = 0
            else:
                frames_since_last_detection[object_name] += 1

        # Check for new detections and speak the object name
        object = ['person','handbag','scissors']
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        for i in range(len(indices)):
            index = indices[i]
            class_id = class_ids[index]
            object_name = classes[class_id]

            return_value, image = cap.read()
            if return_value:
                cv2.imwrite('media/fence/detected_image.jpg', image)
            if object_name not in detected_objects:
                detected_objects.add(object_name)
                if object_name in object:
                    engine.say(f"{object_name} detected......alert...alert")
                engine.runAndWait()
            frames_since_last_detection[object_name] = 0

        # Draw bounding boxes around the detected objects
        indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)
        if len(indices) == 0:
            continue
        for i in indices:
            i = indices[0]
            box = boxes[i]
            left = box[0]
            top = box[1]
            width = box[2]
            height = box[3]
            cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
            cv2.putText(frame,classes[class_id],(boxes[i][0]+10, boxes[i][1]+48),cv2.FONT_HERSHEY_COMPLEX,fontScale=3,color=(0,0,255))

        cv2.imshow("Object Detection", frame)

        latest_image = DetectedImage.objects.latest('timestamp')

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return render(request,'stream_control/detect.html',{'latest_image':latest_image})

def take_actions(request):
    # BLYNK_AUTH = settings.BLYNK_AUTH
    # blynk = blynklib.Blynk(BLYNK_AUTH)
    # pin_number = 'v0'

    # if request.method == 'POST':
    #     django_button_state = request.POST.get('button_state')
    #     if django_button_state=='on':
    #         blynk_switch_state = '1'
    #     else:
    #         blynk_switch_state = '0'

    #     blynk.virtual_write(pin_number,blynk_switch_state)
    # return render(request,'stream_control/detect.html')

    redirect_url = "https://blynk.cloud/dashboard/187471/global/filter/1224701/organization/187471/devices/733897/dashboard"
    return redirect(redirect_url)
