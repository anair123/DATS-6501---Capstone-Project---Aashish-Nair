#01 let's take a look at a synchonous code
'''
import time

start = time.perf_counter()

def sleeping():
    print('Sleeping in 1 second...')
    time.sleep(1)
    print('Done Sleeping')

sleeping()
sleeping()
sleeping()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds...')
'''


'''
#2 lets write the above code using multi-threading
# this is the older and more common way of coding

import time
import threading


start = time.perf_counter()


def sleeping():
    print('Sleeping in 1')
    time.sleep(1)
    print('Done sleeping')

t1 = threading.Thread(target=sleeping)
t2 = threading.Thread(target=sleeping)
t3 = threading.Thread(target=sleeping)

t1.start()
t2.start()
t3.start()

t1.join()
t2.join()
t3.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds...')
'''

'''
#03 lets run the program 10 times

import time
import threading


start = time.perf_counter()


def sleeping():
    print('Sleeping in 1')
    time.sleep(1)
    print('Done sleeping')

threads = []

for _ in range(10):
    t = threading.Thread(target=sleeping)
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

finish = time.perf_counter()

print(f'Finished in {round(finish-start, 2)} seconds...')

'''

'''
#4 lets use parameters


import time
import threading


start = time.perf_counter()


def sleeping(seconds):
    print('Sleeping in {} seconds...'.format(seconds))
    time.sleep(seconds)
    print('Done sleeping')


threads = []

for _ in range(100):
    t = threading.Thread(target=sleeping, args=[1.5])
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} seconds...') 
'''

'''

#5 The better, faster and newer way to work with threads
# available since Python 3.2, this uses the thread pool
# exector and it works with a context manager

import time
import concurrent.futures as cf

start = time.perf_counter()


def sleeping(seconds):
    print('Sleeping in {} seconds...'.format(seconds))
    time.sleep(seconds)
    return 'Done sleeping...' + str(seconds)

with cf.ThreadPoolExecutor() as executor:
    f1 = executor.submit(sleeping, 1.5)
    f2 = executor.submit(sleeping, 2)
    f3 = executor.submit(sleeping, 3)
    print(f1.result())
    print(f2.result())
    print(f3.result())
    
    #to execute functions one at a time, use submit method;
    #it returns a future object which contains information from
    #the function; the result() method contains that information
    #and can be used to display it


finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} seconds...')
    
'''

'''
#06 lets run the above multiple times


import time
import concurrent.futures as cf

start = time.perf_counter()


def sleeping(seconds):
    print('Sleeping in {} seconds...'.format(seconds))
    time.sleep(seconds)
    return 'Done sleeping...' + str(seconds)

with cf.ThreadPoolExecutor() as executor:
    secs = [5,4,3,2,1]
    results = [executor.submit(sleeping, sec) for sec in secs]

    for f in cf.as_completed(results):
        print(f.result())

finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} seconds...')

'''
'''
# 07 using the map() function (execute a function on a list of elements)

import time
import concurrent.futures as cf

start = time.perf_counter()


def sleeping(seconds):
    print('Sleeping in {} seconds...'.format(seconds))
    time.sleep(seconds)
    return 'Done sleeping...' + str(seconds)

with cf.ThreadPoolExecutor() as executor:
    secs = [5,4,3,2,1]
    results = executor.map(sleeping, secs)

    for result in results:
        print(result)

finish = time.perf_counter()
print(f'Finished in {round(finish-start, 2)} seconds...')
'''
'''
#08 a practical use of threading; first the synchronous way

import requests
import time


image_urls = []

t1 = time.perf_counter()

for image_url in image_urls:
    image_bytes = requests.get(image_url)
    image_name = image_url.split('/')[3]
    #print(image_name)
    image_name = 'image_{image_name}.jpg'
    
    with open(image_name, 'wb') as image_file:
        image_file.write(image_bytes)
        print(f'{image_name} was downloaded...')
        
t2 = time.perf_counter()
print(f'Finished in {t2-t1} seconds')

'''

# 09 using threading

import concurrent.futures as cf
import requests
import time

image_urls = []

t1 = time.perf_counter()

def downloaded_image(image_url):
    image_bytes = requests.get(image_url)
    image_name = image_url.split('/')[3]
    # print(image_name)
    image_name = f'image_{image_name}.jpg'

    with open(image_name, 'wb') as image_file:
        image_file.write(image_bytes)
        print(f'{image_name} was downloaded...')

with cf.ThreadPoolExecutor() as executor:
    executor.map(downloaded_image, image_urls)

t2 = time.perf_counter()
print(f'Finished in {t2 - t1} seconds')

