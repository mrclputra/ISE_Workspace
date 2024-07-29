import numpy as np
import cv2

#rgb(175, 192, 200)

bgr_color = np.uint8([[[224, 224, 224]]])

hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)

print("BGR Color: ", np.ravel(bgr_color))
print("HSV Color: ", np.ravel(hsv_color))

lower_limit = hsv_color[0][0][0] - 10, 100, 100
upper_limit = hsv_color[0][0][0] + 10, 255, 255

print("Lower Limit: ", lower_limit)
print("Upper Limit: ", upper_limit)