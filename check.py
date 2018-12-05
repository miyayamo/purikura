import time
f = open("disp.conf", "w")
f.write("q1,1")
f.close()
time.sleep(0.5)
f = open("disp.conf", "w")
f.write("q1,0")
f.close()
time.sleep(5)
