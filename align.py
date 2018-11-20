import numpy as np
import math
import itertools
from common import *

def FormL(points, height=HEIGHT, width=WIDTH):
    u_0, v_0 = points[0][:2]
    u_1, v_1 = points[1][:2]
    u_2, v_2 = points[2][:2]
    u_3, v_3 = points[3][:2]
    # print("(%d %d),(%d %d),(%d %d),(%d %d)" % (u_0, v_0, u_1, v_1, u_2, v_2, u_3, v_3))
    null = np.zeros((3,))
    p_0 = np.array([0, 0, 1])
    p_1 = np.array([0, width-1, 1])
    p_2 = np.array([height-1, 0, 1])
    p_3 = np.array([height-1, width-1, 1])
    L_0 = np.hstack([p_0, null, -u_0 * p_0])
    L_1 = np.hstack([null, p_0, -v_0 * p_0])
    L_2 = np.hstack([p_1, null, -u_1 * p_1])
    L_3 = np.hstack([null, p_1, -v_1 * p_1])
    L_4 = np.hstack([p_2, null, -u_2 * p_2])
    L_5 = np.hstack([null, p_2, -v_2 * p_2])
    L_6 = np.hstack([p_3, null, -u_3 * p_3])
    L_7 = np.hstack([null, p_3, -v_3 * p_3])
    L = np.vstack([L_0, L_1, L_2, L_3, L_4, L_5, L_6, L_7])
    return L

def SEigenVector(L):
    M = np.matmul(L.T, L)
    values, vectors = np.linalg.eig(M)
    sval_idx = np.where(values == np.min(values))
    return values[sval_idx], vectors[:, sval_idx].reshape(-1, 1)    

def GetTransform(points, height=HEIGHT, width=WIDTH):
    L = FormL(points, height, width)
    _, h = SEigenVector(L)
    return h.reshape((3, 3))

def TrInt(x, low, up):
    return int(round(min(max(x, low), up)))

def WrapImage(image, transform, height=HEIGHT, width=WIDTH, scale=2):
    wrapped = np.zeros((height, width), dtype=np.uint8)
    H, W = image.shape[:2]
    for h in range(height):
        for w in range(width):
            p = np.array([h, w, 1])
            q = np.matmul(transform, p)
            u, v = TrInt(q[0]/q[2], 0, H-1), TrInt(q[1]/q[2], 0, W-1)
            # print("%d %d" % (u, v))

            u_around = range(u - scale, u + scale + 1)
            v_around = range(v - scale, v + scale + 1)
            # u_around = [u-2, u-1, u, u+1, u+2]
            # v_around = [v-2, v-1, v, v+1, v+2]
            around = itertools.product(u_around, v_around)
            count = 0.
            total = 0.
            for _a in around:
                try:
                    if image[_a[0]][_a[1]] == 0:
                        count += 1
                        total += 1
                    else:
                        total += 1
                except:
                    continue

            wrapped[h][w] = 0 if count / max(total, 1) > 0.2 else 255
    return wrapped

def TraceRecAux(image, point, direction):
    for _ in range(RECLEN):
        point += direction
        if image[point[0]][point[1]] != 0:
            return False
    return True

def TraceRec(image, corner, height=HEIGHT, width=WIDTH):
    directions = ((corner == 0) * 2 - 1)
    direct_inH = np.array([0, directions[1]])
    direct_inV = np.array([directions[0], 0])
    direct_outH = np.array([0, -directions[1]])
    point = np.copy(corner)
    return (TraceRecAux(image, point, direct_inH) 
        and TraceRecAux(image, point, direct_inV) 
        and TraceRecAux(image, point, direct_outH))

def RecReco(image):
    H, W = image.shape[:2]
    corners = [np.array([0, 0]),
               np.array([0, W-1]),
               np.array([H-1, 0]),
               np.array([H-1, W-1])]

    isRecs = np.zeros((4,), dtype=np.bool)
    for i, corner in enumerate(corners):
        isRecs[i] = TraceRec(image, corner)
    recPos = np.where(isRecs == True)[0]

    _TYPE = -1
    if ES not in recPos:
        return TYPE_0
    if WS not in recPos:
        return TYPE_1
    if WN not in recPos:
        return TYPE_2
    if ES not in recPos:
        return TYPE_3    
    
    return _TYPE

def RotatePoint(point, center, angle):
    if angle == ANGLE_0:
        return point
    if angle == ANGLE_1:
        p_unct = point - center
        return np.array([-p_unct[1], p_unct[0]]) + center  
    if angle == ANGLE_2:
        return center * 2 - point
    if angle == ANGLE_3:
        p_unct = point - center
        return np.array([p_unct[1], -p_unct[0]]) + center 

def RotateImageAux(image, angle, height=HEIGHT, width=WIDTH):
    rotated = np.zeros((height, width), dtype=np.uint8)
    center = np.array([height-1, width-1]) / 2.
    for h in range(height):
        for w in range(width):
            h_r, w_r = RotatePoint(np.array([h, w]), center, angle)[:2]
            rotated[int(h_r)][int(w_r)] = image[h][w]
    return rotated

def RotateImage(image, _TYPE, height=HEIGHT, width=WIDTH):    
    if _TYPE == TYPE_0:
        return np.copy(image)
    if _TYPE == TYPE_1:
        return RotateImageAux(image, ANGLE_1)
    if _TYPE == TYPE_2:
        return RotateImageAux(image, ANGLE_2)
    
    return None

    
    