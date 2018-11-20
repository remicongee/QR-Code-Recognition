import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import itertools
import random

def ShowImage(image):
    plt.imshow(image)
    plt.axis("off")
    plt.show()

def ReadImage(path, threshold=None, kernel_size=3):
    image = cv.imread(path, 0)
    image = GaussBlur(image, kernel_size)
    if threshold == None:
        H, W = image.shape[:2]
        _image = np.reshape(image, [1, H * W])
        threshold = np.mean(_image)
    _, binary = cv.threshold(image, threshold, 255, cv.THRESH_BINARY)
    # ShowImage(binary)
    return binary

def GaussBlur(image, kernel_size=3):
    return cv.GaussianBlur(image, (kernel_size, kernel_size), 0)

def MorphAux(image, pixel_value):
    copy = np.copy(image)
    H, W = image.shape[:2]
    for h in range(H):
        for w in range(W):
            if copy[h][w] == 0:
                h_around = [h-1, h, h+1]
                w_around = [w-1, w, w+1]
                around = itertools.product(h_around, w_around)
                for _a in around:
                    try:
                        image[_a[0]][_a[1]] = 0
                    except:
                        continue

def Dilate(image, iterations):
    dilation = np.copy(image)
    for _ in range(iterations):
        MorphAux(dilation, 0)
        # dilation = cv.erode(dilation, None)
    return dilation

def Erode(image, iterations):
    erosion = np.copy(image)
    for _ in range(iterations):
        MorphAux(erosion, 255)
        # erosion = cv.dilate(erosion, None)
    return erosion

def GetEdges(image):
    H, W = image.shape[:2]
    padded = cv.copyMakeBorder(image, 1, 0, 1, 0, cv.BORDER_REPLICATE)
    ## Get horizontal edges
    crop = padded[:-1, 1:]
    edge_horizontal = crop - image
    for h in range(H):
        for w in range(W):
            if edge_horizontal[h][w] == 1:
                edge_horizontal[h][w] = 0
                edge_horizontal[h-1][w] = 255
    ## Get vertical edges
    crop = padded[1:,:-1]
    edge_vertical = crop - image
    for h in range(H):
        for w in range(W):
            if edge_vertical[h][w] == 1:
                edge_vertical[h][w] = 0
                edge_vertical[h][w-1] = 255

    ## Combine edges
    _, edge = cv.threshold(edge_horizontal + edge_vertical, 1, 255, cv.THRESH_BINARY)
    return edge      

def GenSquare(image, kernel_size=100, shape=cv.MORPH_ELLIPSE, iterations=5):
    kernel = cv.getStructuringElement(shape, (kernel_size, kernel_size))
    square = cv.erode(image, kernel, iterations)
    # ShowImage(square)
    return square

def RecSquare(image, kernel_size=100, shape=cv.MORPH_ELLIPSE, iterations=5):
    kernel = cv.getStructuringElement(shape, (kernel_size, kernel_size))
    QR = cv.dilate(image, kernel, iterations)
    # ShowImage(QR)
    return QR