# -*- coding: utf-8 -*-
import cv2, numpy as np

def gb_crop(path):
    img = cv2.imread(path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV, 3)

    lower = np.array([30,70,70])
    upper = np.array([80,255,255])

    mask_white = cv2.inRange(hsv, lower, upper)
    res_white = cv2.bitwise_or(img, img, mask=mask_white)

    # ネガポジ反転
    nega = cv2.bitwise_not(res_white)

    # グレースケール
    gray = cv2.cvtColor(nega, cv2.COLOR_BGR2GRAY)

    # 二値化
    mat, bw = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # マスク処理
    #マスクをグレースケールで読み込む
    mask = cv2.imread("bw", 0)
    #BGRにチャンネル分解
    bgr = cv2.split(img)
    #透明チャンネル(マスク)を追加
    bgra = cv2.merge(bgr + [bw])
    return bgra
