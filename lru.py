from collections import OrderedDict
from time import time
from itertools import islice

class LRUCachedFunction(object):
    def __init__(self, function, max_size=1024, expiration=15*60):
        self.max_size = max_size
        self.expiration = expiration
        self.function = function

        self.__values = {}
        self.__expire_times = OrderedDict()
        self.__access_times = OrderedDict()
        self.__name__ = function.__name__

    def size(self):
        return len(self.__values)

    def clear(self):
        for k in self.__values.iterkeys():
            self.__del_item(k)

    def __call__(self, *args, **kwargs):
        self.__cleanup()
        key = repr( (args, kwargs) )

        t = int(time())

        if self.__values.has_key(key):
            del self.__access_times[key]
            self.__access_times[key] = t
            return self.__values[key]
        else:
            self.__values[key] = self.function(*args, **kwargs)
            self.__access_times[key] = t
            self.__expire_times[key] = t + self.expiration


    def __del_item(self, key):
        if self.__values.has_key(key):
            del self.__values[key]
            del self.__expire_times[key]
            del self.__access_times[key]

    def __cleanup(self):
        if self.expiration is None:
            return None
        t = int(time())
        #Delete expired
        for k in self.__expire_times.iterkeys():
            if self.__expire_times[k] < t:
                self.__del_item(k)
            else:
                break

        #If we have more than self.max_size items, delete the oldest
        while (len(self.__values) > self.max_size - 1):
            for k in self.__access_times.iterkeys():
                self.__del_item(k)
                break



if __name__=="__main__":
    from time import sleep

    def test(i):
        print 'Calling test with ' + str(i)
        return str(i) + " - result"
    f = LRUCachedFunction(test, 5, 3)
    for i in range(7):
        f(i)
    for i in range(3,7): #This should result in print nothing, since 3-6 are already in the queue
        f(i)
    f(0) #This should result in a print statement, since the 0'th element was removed from the cache due to size issues
    sleep(5)
    print "Continuing"
    for i in range(4): #Cache should be empty, so this should result in prints
        f(i)
    for i in range(4): #But this should not result in anything being printed
        f(i)

