#python -m pip install opencv-python
#python -m pip install opencv-contrib-python
#python -m pip install -U pygame --user
#python -m pip install mysql-connector-python
import cv2, sys, datetime, msvcrt, time, pygame, threading, mysql.connector
from selenium import webdriver
driver = webdriver.Chrome("chromedriver.exe")
driver.get("http://localhost/index.py")


db=mysql.connector.connect(host="127.0.0.1", user="root", password="")
cursor=db.cursor()
cursor.execute("USE rensyu")
db.commit()

def shutter():
    global flag
    global frame
    pygame.mixer.init()
    pygame.mixer.music.load('mp3/countdown.mp3')
    pygame.mixer.music.play(1)
    th1 = threading.Thread(target=flash)
    th1.start()
    time.sleep(4)
    pygame.mixer.music.stop()
    path = datetime.datetime.now().strftime("%Y%m%d-%H%M%S") + ".jpg"
    cv2.imwrite("C:\\xampp\\htdocs\\" + path,frame)




    print(path + "を撮影しました。")
    sql = "INSERT INTO `puri`(`filename`) VALUES ('" + path + "')"
    cursor.execute(sql)
    db.commit()
    flag = 1
    driver.refresh()
def flash():
    time.sleep(3.3)
    global cap
    ret, frame = cap.read()
    flash = cv2.imread("flash.png")
    frame = cv2.addWeighted(frame,0,flash,1,1)
    cv2.imshow("webcam", frame)
    cv2.waitKey(60)


if(cv2.VideoCapture(0).isOpened() is True):
    cap = cv2.VideoCapture(0)
if(cv2.VideoCapture(1).isOpened() is True):
    cap = cv2.VideoCapture(1)



cap.set(cv2.CAP_PROP_FRAME_WIDTH, 960)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 30)
cv2.namedWindow("webcam", cv2.WINDOW_NORMAL)
cv2.moveWindow('webcam', 0, 0)

if (cap.isOpened() is False):
    print("can not open camera")
    sys.exit()

flag = 1
while (1):
    ret, frame = cap.read()
    cv2.imshow("webcam", frame)
    cv2.waitKey(60)

    if (msvcrt.kbhit()):#linuxでうごかない？
        keyevent = ord(msvcrt.getch())+flag
        if (keyevent == 14):
            flag = 0
            th2 = threading.Thread(target=shutter)
            th2.start()


cap.release()
cv2.destroyAllWindows()

# SELECT
# cursor.execute('SELECT * FROM puri')
# rows = cursor.fetchall()
# for i in rows:
#     print(i)
