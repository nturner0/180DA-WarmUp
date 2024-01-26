# I used the code at https://code.likeagirl.io/finding-dominant-colour-on-an-image-b4e075f98097
# as a baseline, and added new features. My code allows a video feed intake, and captures
# the current frame by pressing 'c', which then uses Kmeans to find the dominante colors in a central
# rectangle.

import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans


def find_histogram(clt):
    """
    create a histogram with k clusters
    :param: clt
    :return:hist
    """
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    hist = hist.astype("float")
    hist /= hist.sum()

    return hist
def plot_colors2(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    # return the bar chart
    return bar

cap = cv2.VideoCapture(0)

while(True):
    if cv2.waitKey(1) & 0xFF == ord('c'): #determine Kmeans for current frame and display the histogram

        frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #print(frame.shape): image is 480x640
        center_frame = frame2[100:380, 200:440]

        center_frame = center_frame.reshape((center_frame.shape[0] * center_frame.shape[1],3)) #represent as row*column,channel number
        clt = KMeans(n_clusters=3) #cluster number
        clt.fit(center_frame)

        hist = find_histogram(clt)
        bar = plot_colors2(hist, clt.cluster_centers_)

        plt.axis("off")
        plt.imshow(bar)
        plt.show()

    if cv2.waitKey(1) & 0xFF == ord('q'):   #q to quit
        break

    ret, frame = cap.read()
    frame_rect = frame.copy()   #create a separate display frame so the rectangle does not interfere with Kmeans
    cv2.rectangle(frame_rect,(200,100),(440,380),(0,255,0),2) #draw bounding rectangle
    cv2.imshow('Video Feed', frame_rect)

cap.release()
cv2.destroyAllWindows()