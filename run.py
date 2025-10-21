import multiprocessing
import subprocess

# Process 1: Strat Friday
def startFriday():
    print("Process 1 is running...")
    from main import start
    start()

# Process 2: To run the hotWord
def listenHotword():
    print("Process 2 is running....")
    from engine.features import hotword
    hotword()

# To start both the processes
if __name__=='__main__':
    p1 = multiprocessing.Process(target=startFriday)
    p2 = multiprocessing.Process(target=listenHotword)
    p1.start()
    subprocess.call([r'device.bat'])
    p2.start()
    p1.join()

    if p2.is_alive():
        p2.terminate()
        p2.join()

    print("System stop")