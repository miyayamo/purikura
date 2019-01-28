#conf[menu, shutter, gbselect, print]
#python -m pip install opencv-python
#python -m pip install opencv-contrib-python
#python -m pip install -U pygame --user
#python -m pip install mysql-connector-python
import cv2, sys, datetime, msvcrt, time, pygame, threading, subprocess, numpy as np
from PIL import Image

if(cv2.VideoCapture(0).isOpened() is True):
    cap = cv2.VideoCapture(0)
if(cv2.VideoCapture(1).isOpened() is True):
    cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)
cv2.namedWindow("webcam", cv2.WINDOW_NORMAL)
cv2.setWindowProperty("webcam", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

if (cap.isOpened() is False):
    print("can not open camera")
    sys.exit()


def addpointer(x, y):
    img_po = cv2.circle(background, (x, y), 25, (255, 255, 0, 0), -1)
    return img_po

def readpointconf():
    global point_conf
    f = open("point.conf", "r")
    point_conf = f.read().split(",")
    f.close()

def poswrite():
    try:
        readpointconf()
        background = addpointer(int(point_conf[0]), int(point_conf[1]))
        print (point_conf)
    except Exception as e:
        print (e, 'error occurred')

def img_print(maskedpath):
    subprocess.run("mspaint {} /p".format(maskedpath))
    print("印刷：".format(maskedpath))

def add_alpha(data):
    rgba = cv2.cvtColor(data, cv2.COLOR_RGB2RGBA)
    return rgba

def readconf():
    global disp_conf
    f = open("disp.conf", "r")
    disp_conf = f.read().split(",")
    f.close()

def add(fg, bg, x, y):
    global background
    height, width = fg.shape[:2]
    bg[y:height + y, x:width + x] = fg
    background = bg

def add2(bg):
    global background
    time.sleep(0.5)
    img1 = cv2.imread("bg/bg{}.png".format(str(bg).zfill(2)), -1)
    img2 = cv2.imread("out.png", -1)
    print("選択：bg{}".format(str(bg).zfill(2)))

    amask = img2[:,:,3]
    amask_inv = cv2.bitwise_not(amask)

    img1_bg = cv2.bitwise_and(img1,img1,mask = amask_inv)
    img2_fg = cv2.bitwise_and(img2,img2,mask = amask)

    background = cv2.add(img1_bg,img2_fg)
    background = add_alpha(background)
    cv2.imwrite("masked/" + path[6:], background)#ここでうまく書き込めないのが原因

def confedit(text):
    f = open("disp.conf", "w")
    f.write(text)
    f.close()

def scenesetup():
    global frame
    confedit("q1,1,0,0,")
    ret, frame = cap.read()#反転させるには「cv2.flip(img, 1)」
    frame = cv2.flip(frame, 1)

def menu1():
    global background, foreground, frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    background = add_alpha(frame)
    foreground = cv2.imread('img/button1.png', -1)#730,570 930x690
    add(foreground, background, 880, 570)
    poswrite()
    frame = background

addflag = False
addbg = 1
def menu2():#二回目の撮影でbackgroundがおかしくなる※ここが原因！！
    global background, foreground, frame, addflag, addbg
    background = cv2.imread("out.png", -1)
    if(disp_conf[2] != "0"):
        addbg = addbg + int(disp_conf[2])
        addflag = False
        confedit("q2,0,0,0,")
    if(addflag == False):
        add2(addbg)
        addflag = True
    else:
        background = cv2.imread("masked/" + path[6:], -1)

    # foreground = cv2.imread('img/button2.png', -1)#30,570 230x690
    # add(foreground, background, 190, 570)
    foreground = cv2.imread('img/button3.png', -1)#730,570 930x690
    add(foreground, background, 880, 570)
    foreground = cv2.imread('img/button4.png', -1)#30,300 150,420
    add(foreground, background, 190, 300)
    foreground = cv2.imread('img/button5.png', -1)#810,300 930,420
    add(foreground, background, 960, 300)
    poswrite()
    frame = background

def menu3():
    global background, foreground, frame
    background = cv2.imread("masked/" + path[6:], -1)
    if(disp_conf[3] == "1"):
        img_print("masked\\" + path[6:])
        confedit("q3,0,0,0,")
    foreground = cv2.imread('img/button6.png', -1)#730,570 930x690
    add(foreground, background, 190, 570)
    foreground = cv2.imread('img/button7.png', -1)#30,570 230x690
    add(foreground, background, 880, 570)
    poswrite()
    frame = background

def menu():
    global background, foreground, frame
    if (disp_conf[0] == "0"):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
    elif (disp_conf[0] == "q1"):
        menu1()
    elif (disp_conf[0] == "q2"):
        menu2()
    elif (disp_conf[0] == "q3"):
        menu3()

    cv2.imshow("webcam", frame)
    cv2.waitKey(30)

def anime():
    global background, foreground, frame
    if (disp_conf[0] == "0"):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
    elif(disp_conf[0] == "1"):
        menu1()
        foreground = cv2.imread('img/button1.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 880, 570)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    elif(disp_conf[0] == "2"):
        menu2()
        foreground = cv2.imread('img/button2.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 190, 570)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    elif(disp_conf[0] == "3"):
        menu2()
        foreground = cv2.imread('img/button3.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 880, 570)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    elif(disp_conf[0] == "4"):
        menu2()
        foreground = cv2.imread('img/button4.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 190, 300)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    elif(disp_conf[0] == "5"):
        menu2()
        foreground = cv2.imread('img/button5.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 960, 300)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    elif(disp_conf[0] == "6"):
        menu3()
        foreground = cv2.imread('img/button6.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 190, 570)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    elif(disp_conf[0] == "7"):
        menu3()
        foreground = cv2.imread('img/button7.png', -1)
        cond_p = (foreground[..., 0] <= 100) & (foreground[..., 1] <= 100) & (foreground[..., 2] <= 100)
        foreground[cond_p] = [150, 150, 150, 0]
        add(foreground, background, 880, 570)
        frame = background
        cv2.imshow("webcam", frame)
        cv2.waitKey(30)
    else:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

flashimg = cv2.imread("img/flash.png")
def flash():
    # time.sleep(3.3)
    global cap, flashimg
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.addWeighted(frame,0,flashimg,1,1)
    cv2.imshow("webcam", frame)

def shutter():
    global shutterflag, frame, path
    pygame.mixer.init()
    pygame.mixer.music.load('img/countdown.mp3')
    pygame.mixer.music.play(1)
    time.sleep(3.4)
    flash()
    time.sleep(0.1)
    pygame.mixer.music.stop()
    path = "photo/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".png"
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite(".\\" + path,frame)
    print("撮影：{}".format(path))
    confedit("q2,0,0,0,")
    shutterflag = 1
    addflag = False

    cv2.imwrite("out.png", gb_crop(path))

    menu2()

def ifshutter():
    global shutterflag
    while True:
        time.sleep(0.05)
        readconf()
        try:
            if (disp_conf[1] == "1" and (disp_conf[0] == "q1" or disp_conf[0] == "1") and shutterflag == 1):
                shutterflag = 0

                th2 = threading.Thread(target=shutter)
                th2.start()
        except:
            print("\r")

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

scenesetup()
shutterflag = 1
ths = threading.Thread(target=ifshutter)
ths.start()


while True:
    readconf()
    menu()
    anime()


cap.release()
cv2.destroyAllWindows()
