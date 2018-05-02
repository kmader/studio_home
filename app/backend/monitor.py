import sys
from multiprocessing import Process
import backend.run as run
import backend.test as test

if __name__ == '__main__':
    if sys.argv[1] == "train":
        child_process = Process(target=run.main, args=(sys.argv[2], sys.argv[3], sys.argv[4]))
        del sys.argv[0]
        run.monitor(child_process)
    elif sys.argv[1] == 'test':
        child_process = Process(target=test.main, args=(sys.argv[2], sys.argv[3], sys.argv[4]))
        del sys.argv[0]
        test.monitor(child_process)
   
