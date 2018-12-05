#python -m pip install opencv-python
#python -m pip install opencv-contrib-python
#python -m pip install -U pygame --user
#python -m pip install mysql-connector-python
import cv2, sys, datetime, msvcrt, time, pygame, threading, numpy as np
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


def readconf():
    global disp_conf
    f = open("disp.conf", "r")
    disp_conf = f.read().split(",")
    f.close()

def clip_alpha_image(x,y):
    #x,yで貼り付け位置を選択
    f_h, f_w, _ = foreground.shape
    #透明部分が0、不透明部分が1のマスクを作る
    alpha_mask = np.ones((f_h, f_w)) - np.clip(cv2.split(foreground)[3],0,1)
    #貼り付ける位置の背景部分
    target_background = background[y:y+f_h,x:x+f_w]
    #各BRGチャンネルにalpha_maskを掛けて、前景の不透明部分が[0, 0, 0]のnew_backgroundを作る
    new_background = cv2.merge(list(map(lambda x:x * alpha_mask,cv2.split(target_background))))
    #BGRAをBGRに変換した画像とnew_backgroundを足すと合成できる
    background[y:y + f_h,x:x+f_w] = cv2.merge(cv2.split(foreground)[:3]) + new_background

def scenesetup():
    global frame
    ret, frame = cap.read()#反転させるには「cv2.flip(img, 1)」
    frame = cv2.flip(frame, 1)

def menu1():
    global background, foreground, frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    background = frame
    foreground = cv2.imread('img/button1.png', -1)#730,570 930x690
    clip_alpha_image(880, 570)
    frame = background

gbimg = np.array(Image.open("gb.jpg"))
def menu2():
    global background, foreground, frame, gbimg
    frame = gbimg
    background = frame
    foreground = cv2.imread('img/button2.png', -1)#30,570 230x690
    clip_alpha_image(190, 570)
    foreground = cv2.imread('img/button3.png', -1)#730,570 930x690
    clip_alpha_image(880, 570)
    foreground = cv2.imread('img/button4.png', -1)#30,300 150,420
    clip_alpha_image(190, 300)
    foreground = cv2.imread('img/button5.png', -1)#810,300 930,420
    clip_alpha_image(960, 300)
    frame = background

def menu3():
    global background, foreground, frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    background = frame
    foreground = cv2.imread('img/button6.png', -1)#730,570 930x690
    clip_alpha_image(880, 570)
    foreground = cv2.imread('img/button7.png', -1)#30,570 230x690
    clip_alpha_image(190, 570)
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
    global background, foreground, frame, gbimg#メニュー2のアニメーションがうまくいかない
    dirpath = "anime/anime_"
    dirpath2 = "anime/anime2_"
    if (disp_conf[0] == "0"):
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
    elif(disp_conf[0] == "1"):
        for i in range(23):
            menu1()
            filepath = dirpath + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(870, 560)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)
    elif(disp_conf[0] == "2"):
        for i in range(23):
            menu2()
            filepath = dirpath + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(180, 560)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)
    elif(disp_conf[0] == "3"):
        for i in range(23):
            menu2()
            filepath = dirpath + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(870, 560)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)
    elif(disp_conf[0] == "4"):
        for i in range(23):
            menu2()
            filepath = dirpath2 + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(180, 290)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)
    elif(disp_conf[0] == "5"):
        for i in range(23):
            menu2()
            filepath = dirpath2 + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(950, 290)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)
    elif(disp_conf[0] == "6"):
        for i in range(23):
            menu3()
            filepath = dirpath + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(180, 560)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)
    elif(disp_conf[0] == "7"):
        for i in range(23):
            menu3()
            filepath = dirpath + str(i).zfill(4) + ".png"
            foreground = cv2.imread(filepath, -1)
            clip_alpha_image(870, 560)
            frame = background
            cv2.imshow("webcam", frame)
            cv2.waitKey(30)

flashimg = cv2.imread("flash.png")
def flash():
    # time.sleep(3.3)
    global cap, flashimg
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.addWeighted(frame,0,flashimg,1,1)
    cv2.imshow("webcam", frame)

def shutter():
    global shutterflag, frame, gbimg
    pygame.mixer.init()
    pygame.mixer.music.load('mp3/countdown.mp3')
    pygame.mixer.music.play(1)
    time.sleep(3.3)
    flash()
    time.sleep(0.6)
    pygame.mixer.music.stop()
    path = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2.imwrite(".\\" + path,frame)
    print("\n" + path + "を撮影しました。")
    shutterflag = 1
    gbimg = np.array(Image.open(path))

def ifshutter():
    global shutterflag
    while True:
        time.sleep(0.05)
        readconf()
        print(disp_conf)
        try:
            if (disp_conf[1] == "1" and shutterflag == 1):
                shutterflag = 0
                th2 = threading.Thread(target=shutter)
                th2.start()
            else:
                print("\r{}".format("撮影待機中"), end="")
        except:
            f = open("error", "w")
            f.close()

scenesetup()
shutterflag = 1
ths = threading.Thread(target=ifshutter)
ths.start()
while True:

    readconf()
    menu()
    anime()
    # if (msvcrt.kbhit()):#linuxでうごかない？
    #     keyevent = ord(msvcrt.getch())+shutterflag
    #     if (keyevent == 14):
    #         shutterflag = 0
    #         th2 = threading.Thread(target=shutter)
    #         th2.start()


cap.release()
cv2.destroyAllWindows()
