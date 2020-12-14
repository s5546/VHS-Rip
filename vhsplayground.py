# we testin multiplication / division speeds
import threading
import random
import time

def multiply(ints):
   print("mul     started")
   start = time.time()
   procNums = []
   for i in range (len(ints)): 
      procNums.append(ints[i] * 2)
   print("mul     ", time.time() - start)
   
   

def divide(ints):
   print("div     started")
   start = time.time()
   procNums = []
   for i in range (len(ints)):
      procNums.append(ints[i] / 2)
   print("div     ", time.time() - start)

random.seed("we rippin VHSes")
nums = []
print("main    generating")
start = time.time()
for i in range(100000000):
   nums.append(random.randint(10, 100))
   if i % 10000000 == 0:
      print(i/1000000, "% done")
print("100.0 % done")
print("main    ", time.time() - start)

multiply(nums)
divide(nums)
#threading.Thread(target=multiply, args=(nums,)).start()
#threading.Thread(target=divide, args=(nums,)).start()
#time.sleep(100)