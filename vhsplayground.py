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


floatie = 0.12345678901234567890
print(str(floatie))
print(abs(5-10))


'''
HHMMSS = "99:20:15"
hms_array = HHMMSS.split(":")
if (len(hms_array) == 2): # if its MM:SS
    hms_array.insert(0, "00")
# todo: see if this section breaks if hours > 24
temp_range = len(hms_array)
temp_seconds = 0
for i in range(temp_range):
   temp_seconds = temp_seconds + (int(hms_array[i]) * (60 ** (temp_range - 1 - i)))
   print(temp_seconds)




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
'''