import random
import time
4
person = ["강승현", "구현모","다희","김영서","지수","태헌","혜민","혜주","상우"
          ,"석주","혜원언냐","작은혜원","상욱","수지","예진","지현"]

count = 16
num = 4

for i in range(1, int(count/num) + 1):
    print(i)
    for n in range(1,num + 1):
        q=random.choice(person)
        person.remove(q)
        print(q)
    
