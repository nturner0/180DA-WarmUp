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

    # Capture frame-by-frame
    ret, frame = cap.read()
    # HSV Image
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Mask bounds
    lower_bound = np.array([80,50,50])
    upper_bound = np.array([110,255,255])

    # Threshold the HSV image to get only pencil colors
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    res = cv2.bitwise_and(frame,frame, mask= mask)

    # Get pencil contours, use mask since it is grayscale
    ret,thresh = cv2.threshold(mask,127,255,0)
    contours,hierarchy = cv2.findContours(thresh, 1, 2)

    # Ensure there is at least one contour
    if len(contours) > 0:
        cnt = contours[0]

        # Find largest contour - this is likely the notebook outline
        max_area = 0
        max_contour = contours[0]
        for c in contours:
            area = cv2.contourArea(c)
            if (area > max_area):
                max_area = area
                max_contour = c
        x,y,w,h = cv2.boundingRect(max_contour)
        # Draw bounding rectangle in original image
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('res',res)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()