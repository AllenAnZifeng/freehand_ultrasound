import cv2
from typing import List
import numpy as np


NUMBER_OF_PICTURES = 50
STARTING_NUMBER = 108
PICTURE_ADDRESS= "data/azf_labelled/trial1/frame%d.jpg"

def video_to_images(address):
    vidcap = cv2.VideoCapture(address) #'video.avi'
    success, image = vidcap.read()

    count = 0
    # print(type(image), image.shape)
    row, col, _ = image.shape

    while success:
        image = image[:, 80:col - 80]
        cv2.imwrite("frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1


def get_image_bright_locations_filled(address, z_value) -> List[List[int]]:
    res = []
    img = cv2.imread(address, cv2.IMREAD_GRAYSCALE)  # type: np.ndarray
    row, col = img.shape
    img= img[:, 80:col - 80]
    row, col = img.shape
    # 0 --> black, 255 --> white  color representation
    ret, filtered_image = cv2.threshold(img, 240, 255, cv2.THRESH_BINARY)
    # filtered_image 0 -->black

    contours = np.empty((1,2),np.int8)
    for r in range(row):
        for c in range(col):
            if filtered_image[r][c] > 0:
                contours= np.vstack((contours, np.array([c,r])))
    cv2.fillPoly(filtered_image, pts=[contours], color=(255,255,255))

    for r in range(row):
        for c in range(col):
            if filtered_image[r][c] > 0:
                res.append([r, c, z_value])

    # cv2.imwrite('00mytry.png',filtered_image)
    return res


def get_image_bright_locations(address, z_value) -> List[List[int]]:
    res = []
    img = cv2.imread(address, cv2.IMREAD_GRAYSCALE)  # type: np.ndarray
    row, col = img.shape
    img = img[:, 80:col - 80]
    row, col = img.shape
    # 0 --> black, 255 --> white  color representation
    ret, filtered_image = cv2.threshold(img, 220, 255, cv2.THRESH_BINARY)
    # filtered_image 0 -->black

    for r in range(row):
        for c in range(col):
            if filtered_image[r][c] > 0:
                res.append([r, c, z_value])

    cv2.imwrite('00mytry.png',filtered_image)
    return res

def get_all_bright_locations() -> List[List[List[int]]]:
    res = []
    for i in range(STARTING_NUMBER,NUMBER_OF_PICTURES+STARTING_NUMBER):
        print("frame%d.jpg" % i)
        res.append(get_image_bright_locations(PICTURE_ADDRESS % (i), i-STARTING_NUMBER+1))
    return res


def write_to_file(img_list):

    x = []
    y = []
    z = []

    with open('xyz_file/trial1_azf.xyz', 'w') as file:
        for img_num in range(len(img_list)):
            for pt_num in range(len(img_list[img_num])):
                x.append([img_list[img_num][pt_num][0]])
                y.append([img_list[img_num][pt_num][1]])
                z.append([img_list[img_num][pt_num][2]])
                file.write(str(img_list[img_num][pt_num][0]) + ' ' +str(img_list[img_num][pt_num][1]) + ' ' + str(img_list[img_num][pt_num][2]) + '\n')


if __name__ == '__main__':
    # video_to_images()
    # res = get_image_bright_locations('data/azf_labelled/trial1/frame118.jpg',1)
    # print(res)
    write_to_file(get_all_bright_locations())

