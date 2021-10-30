import cv2
import numpy as np


for i in range(4*8*2):
    image = cv2.imread("marbles_large/{}.png".format(i), cv2.IMREAD_UNCHANGED)
    mask = image[:, :, -1]
    kernel = np.ones((4, 4), np.uint8)
    mask = cv2.erode(mask, kernel)

    small = cv2.resize(image, (40, 40), interpolation=cv2.INTER_AREA)
    small_mask = cv2.resize(mask, (40, 40), interpolation=cv2.INTER_AREA)
    small[:, :, -1] = small_mask

    cv2.imwrite("marbles/{}.png".format(i), small)
