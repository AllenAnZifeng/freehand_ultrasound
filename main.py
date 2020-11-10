# fuck you

import json

import matplotlib.pyplot as plt
import numpy as np
import cv2
from typing import List
import scipy.io
from mayavi import mlab
from scipy.spatial import Delaunay
import vtk

import numpy as np
import open3d as o3d


def plotting(image_list: List[List[List[int]]]):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = []
    x = []
    y = []

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
    vidcap = cv2.VideoCapture('hand_labelled.avi')
    success, image = vidcap.read()

    count = 0
    print(type(image), image.shape)
    row, col, _ = image.shape

    while success:
        image = image[:, 80:col - 80]
        cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1


def get_image_bright_locations(address, z_value) -> List[List[int]]:
    res = []
    img = cv2.imread(address, cv2.IMREAD_GRAYSCALE)  # type: np.ndarray
    row, col = img.shape
    # 0 --> white, 255 --> black  color representation
    ret, filtered_image = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    # filtered_image 0 -->black

    for r in range(row):
        for c in range(col):
            if filtered_image[r][c] > 0:
                res.append([r, c, z_value])


    avg_x,avg_y = calculate_image_center(res)
    offset_x,offset_y = base_center[0]-avg_x,base_center[1]-avg_y
    for i in range(len(res)):
        res[i][0] +=offset_x
        res[i][1] +=offset_y

    cv2.imwrite('00mytry.png',filtered_image)
    return res

def get_image_bright_locations_base_image(address, z_value):
    res = []
    img = cv2.imread(address, cv2.IMREAD_GRAYSCALE)  # type: np.ndarray
    row, col = img.shape
    ret, filtered_image = cv2.threshold(img, 250, 255, cv2.THRESH_BINARY)
    for r in range(row):
        for c in range(col):
            if filtered_image[r][c] > 0:
                res.append([r, c, z_value])


    return res

def calculate_image_center(res):
    print('res',res)
    print(res[0])
    print(res[0][0])
    x = [ point[0] for point in res]
    y = [ point[1] for point in res]
    avg_x=sum(x)/len(x)
    avg_y = sum(y)/len(y)
    return avg_x,avg_y


def get_all_bright_locations(count) -> List[List[List[int]]]:
    res = []
    for i in range(count):
        res.append(get_image_bright_locations("frame%d.jpg" % i, i))
    return res

def base_center_point():
    res = get_image_bright_locations_base_image("frame0.jpg",0)
    return calculate_image_center(res)

def write_to_file(img_list):

    x = []
    y = []
    z = []

    with open('3d_coordinate.xyz', 'w') as file:
        for img_num in range(len(img_list)):
            for pt_num in range(len(img_list[img_num])):
                x.append([img_list[img_num][pt_num][0]])
                y.append([img_list[img_num][pt_num][1]])
                z.append([img_list[img_num][pt_num][2]])
                file.write(str(img_list[img_num][pt_num][0]) + ' ' +str(img_list[img_num][pt_num][1]) + ' ' + str(img_list[img_num][pt_num][2]) + '\n')


def testing_git():
    print('learning git')

if __name__ == '__main__':

    base_center = base_center_point()
    # print(base_center)
    # video_to_images()
    # res = get_image_bright_locations('frame71.jpg',1)
    # print(res)

    img_list = get_all_bright_locations(91)
    write_to_file(img_list)
    # print(img_list)
    # stlcreator(img_list)
    # scipy.io.savemat('00data.mat', mdict={'img_list': img_list})

    # plotting(img_list)

    pass


