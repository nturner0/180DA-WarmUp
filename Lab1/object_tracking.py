# I used the code at https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html as a baseline
# for capturing a video and filtering by color/thresholding, and the code at
# https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html as a baseline for generating a 
# bounding box based on contours.
# I added a check to ensure there is at least one contour, and I find the largest contour and draw
# a rectangle around that, assuming the largest contour will be the object we are trying to detect.
# I altered the code to detect for a light blue notebook I was using.

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):

    #Goal: Track a wooden pencil

    # Code to find yellow hue bounds
    # yellow = np.uint8([[[255,255,0 ]]])
    # hsv_yellow = cv2.cvtColor(yellow,cv2.COLOR_BGR2HSV)
    # print(hsv_yellow)
    # Result: 90, use 80 and 100 as lower/upper bounds

    # lower_yellow = np.array([80,50,50])
    # upper_yellow = np.array([100,255,255])

    # The above did not work, since the pencil is not this value of yellow
    # Found that two faces of the pencil in the current enviornment are RGB: (238, 150, 85)
    # and (184, 98, 47) using a screen capture and online color picker

    # color1 = np.uint8([[[238,150,0 ]]])
    # color2 = np.uint8([[[184,98,47 ]]])
    # hsv_color1 = cv2.cvtColor(color1,cv2.COLOR_BGR2HSV)
    # hsv_color2 = cv2.cvtColor(color2,cv2.COLOR_BGR2HSV)
    # print(hsv_color1)
    # print(hsv_color2)

    # Result: (101, 255, 238), and (109, 190, 184)
    # Using [91, 119] for hue bounds, as it is +-10 from experimental value

    # That didn't work either, experimentally hue = [5,15] works well, using that

    # The pencil is annoyingly close to skin hue, switching goal to a blue notebook
    # The box tracks the notebook quite well, even with other objects in frame and different
    # lighting configurations.

    # Capture frame-by-frame
    ret, frame = cap.read()

    # HSV and RGB Images
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    rgb = frame

    # Mask bounds
    hsv_lower_bound = np.array([80,50,50])
    hsv_upper_bound = np.array([110,255,255])

    rgb_lower_bound = np.array([0,150,0])
    rgb_upper_bound = np.array([255,255,255])

    # Threshold the images to get only notebook colors
    hsv_mask = cv2.inRange(hsv, hsv_lower_bound, hsv_upper_bound)
    hsv_res = cv2.bitwise_and(frame,frame, mask= hsv_mask)

    rgb_mask = cv2.inRange(rgb, rgb_lower_bound, rgb_upper_bound)
    rgb_res = cv2.bitwise_and(frame,frame, mask= rgb_mask)

    # Get notebook contours, use mask since it is grayscale
    hsv_ret,hsv_thresh = cv2.threshold(hsv_mask,127,255,0)
    hsv_contours,hsv_hierarchy = cv2.findContours(hsv_thresh, 1, 2)

    rgb_ret,rgb_thresh = cv2.threshold(rgb_mask,127,255,0)
    rgb_contours,rgb_hierarchy = cv2.findContours(rgb_thresh, 1, 2)

    hsv_frame = frame.copy()
    # Ensure there is at least one contour
    if len(hsv_contours) > 0:
        cnt = hsv_contours[0]

        # Find largest contour - this is likely the notebook outline
        max_area = 0
        max_contour = hsv_contours[0]
        for c in hsv_contours:
            area = cv2.contourArea(c)
            if (area > max_area):
                max_area = area
                max_contour = c
        x,y,w,h = cv2.boundingRect(max_contour)
        # Draw bounding rectangle
        cv2.rectangle(hsv_frame,(x,y),(x+w,y+h),(0,255,0),2)

    rgb_frame = frame.copy()
    # Ensure there is at least one contour
    if len(rgb_contours) > 0:
        cnt = rgb_contours[0]

        # Find largest contour - this is likely the notebook outline
        max_area = 0
        max_contour = rgb_contours[0]
        for c in rgb_contours:
            area = cv2.contourArea(c)
            if (area > max_area):
                max_area = area
                max_contour = c
        x,y,w,h = cv2.boundingRect(max_contour)
        # Draw bounding rectangle in original image
        cv2.rectangle(rgb_frame,(x,y),(x+w,y+h),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('HSV Masking', hsv_frame)
    cv2.imshow('RGB Masking', rgb_frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()