#### I/O Bound & CPU Bound Operations ####

# CPU Bound - lot of mem is consumed, heavy tasks/ image processing, large math caluculations, 
# video encoding, some ML related work
# for i in range(1,10000000):
#     print(i)

# I/O Bound - depending on soem external factors - opeing files, time.sleep(), api calls
# import os
# import time
# time.sleep()
# import requests
# requests.get("Hello")

# core - thread , 1 core = 1 tread , 2 code = 2 thread, quad, octa etc.


import threading
import time

# GIL - GLobal Locak Interpreter - GIL allows only single thread to run at a time evwn on the muticore system
# Cpython doesn;t allow to run more than sinlge thread to run you compied python code/bytecode
# why ?, lets say you dfined a list a and did b = a, so if there would have been multipel threads
# same object will be pointed by 2 references and lets say you made changes parallely (true parallel)
# within miliseconds, in both the list
# a[0] = 100, and b[0] = 1000, it will clash

# multithreading - I/O bound task - these oeprations free up cpu for a while, other tasks can be performed
# that means t1 is puased for the time being, t2 can be up and so on t2 to t1 . wicth b.w threads
# so most of the times, taks is waiting not calculating so no load on cpu hence no cpu bound called i/o

# main thread
def task(name):
    for i in range(1,6): # very small loop
        print(name, i)  
        time.sleep(i) # pausing cpu for the timebeing, during sleep CPU is free and can perfom other tasks

# task("A")

## Concurrency- Switcing of thread when other thread sleeping but at a time only on thread will work
print("start")

t1 = threading.Thread(target=task, args=("Thread-1",))
t2 = threading.Thread(target=task, args=("Thread-2",))

t1.start()
# t1.join() # start mandat
print("Completed")

t2.start()