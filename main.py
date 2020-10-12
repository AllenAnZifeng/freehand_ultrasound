import json

import matplotlib.pyplot as plt
import numpy as np
import cv2
from typing import List
import scipy.io



def plotting(image_list:List[List[List[int]]]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = []
    x= []
    y= []

    for i in range(len(image_list)):
        for point in image_list[i]:
            x.append(point[0])
            y.append(point[1])
            z.append(i)

    ax.scatter(x, y, z, marker='o')

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')

    plt.show()


def video_to_images():
    vidcap = cv2.VideoCapture('forearm.avi')
    success, image = vidcap.read()

    count =0
    print(type(image), image.shape)
    row, col, _ = image.shape

    while success:
        image = image[:, 80:col - 80]
        cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1


def get_image_bright_locations(address)->List[List[int]]:
    res = []
    img = cv2.imread(address, cv2.IMREAD_GRAYSCALE)  # type: np.ndarray
    row, col = img.shape
    # 0 --> white, 255 --> black  color representation
    ret, filtered_image = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    # filtered_image 0 -->black

    for r in range(row):
        for c in range(col):
            if filtered_image[r][c] > 0:
                res.append([r, c])

    # cv2.imwrite('00mytry.png',filtered_image)
    return res

def get_all_bright_locations(count)->List[List[List[int]]]:
    res=[]
    for i in range(count):
        res.append(get_image_bright_locations("frame%d.jpg" % i))
    return res


if __name__ == '__main__':
    # video_to_images()
    # res = get_image_bright_locations('frame10.jpg')
    # print(res)

    # img_list = get_all_bright_locations(30)
    # scipy.io.savemat('00data.mat', mdict={'img_list': img_list})

    # plotting(img_list)
    pass