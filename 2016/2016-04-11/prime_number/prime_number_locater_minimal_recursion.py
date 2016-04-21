#!/usr/bin/python3
import math
import time
def Prime_Number_Locater(start, end):
    prime_number_list = []
    if start < 2:
        start = 2    
    for i in range(start, end):
        for j in range(2, int(math.sqrt(i)+1)):
            if i % j == 0:            
                break
        else:
            prime_number_list.append(i)
    return prime_number_list

if __name__ == "__main__":
    first = int(input("First number:"))
    last = int(input("Last number:"))

    start_time = time.time()
    prime_list = Prime_Number_Locater(first, last)
    print("Time taken: {} seconds".format(time.time()-start_time))
    print("Total prime numbers located: {}".format(len(prime_list)))
    #print(prime_list)
#14
#7
#5
#0.03
#Time taken: 0.0016529560089111328
#[10000019, 10000079]


