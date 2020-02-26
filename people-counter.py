import numpy as np
import requests
import time

import cv2


TOKEN = "your token id"  # Put your TOKEN here
DEVICE_LABEL = "machine"  # Put your device label here 
VARIABLE_LABEL_1 = "people"  # Put your first variable label here

faceCascade = cv2.CascadeClassifier(r'H:\facerec/txt.xml')
video_capture  =cv2.VideoCapture(0)
#frame.release()
#cv2.destroyAllWindows()

def build_payload(variable_1):

	while(True):
		idx=0

		ret, frame = video_capture.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = faceCascade.detectMultiScale(
			gray,
			scaleFactor=1.1,
			minNeighbors=5,
			minSize=(30, 30)
        	#flags = cv2.CV_HAAR_SCALE_IMAGE
		)
		for (x,y,w,h) in faces:
			cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
			idx += 1
			print ("number of faces =", idx)
			cv2.putText(frame,str(idx),(x,y+h),cv2.FONT_HERSHEY_SIMPLEX,.7,(150,150,0),2)
			cv2.imshow('img',frame)
			if(cv2.waitKey(1)==ord('q')):
				break
		#break
    # Creates two random values for sending data

		

		value_1 = idx
    	#value_2 = random.randint(0, 85)
		payload = {variable_1: value_1}
		return payload

def post_request(payload):
    # Creates the headers for the HTTP requests
    url = "http://things.ubidots.com"
    url = "{}/api/v1.6/devices/{}".format(url, DEVICE_LABEL)
    headers = {"X-Auth-Token": TOKEN, "Content-Type": "application/json"}

    # Makes the HTTP requests
    status = 400
    attempts = 0
    while status >= 400 and attempts <= 5:
        req = requests.post(url=url, headers=headers, json=payload)
        status = req.status_code
        attempts += 1
        time.sleep(1)

    # Processes results
    if status >= 400:
        print("[ERROR] Could not send data after 5 attempts, please check \
            your token credentials and internet connection")
        return False

    print("[INFO] request made properly, your device is updated")
    return True


def main():
    payload = build_payload(VARIABLE_LABEL_1)

    print("[INFO] Attemping to send data")
    post_request(payload)
    print("[INFO] finished")


if __name__ == '__main__':
    while (True):
        main()
        time.sleep(1)