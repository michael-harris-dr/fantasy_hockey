from random import randrange
import os
import time
os.system("color 20")
i = 0
k = 0
while(k < 200):
    i = 0
    while (i < randrange(100) + 30):
        print(randrange(2), end='')
        i = i + 1
    time.sleep(0.1)
    print("\n")
    k = k + 1