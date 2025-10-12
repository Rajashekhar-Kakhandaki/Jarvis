import multiprocessing


def startJarvis():
    print ("Process 1 Starting...")
    from main import start
    start()
    
def listenHotword():
    print ("Process 2 Starting...")
    from backend.feature import hotword
    hotword()
    
if __name__ == "__main__":
    process1 = multiprocessing.Process(target=startJarvis)
    process2 = multiprocessing.Process(target=listenHotword)
    process1.start()
    process2.start()
    try:
        process1.join()
        process2.join()
    except KeyboardInterrupt:
        print("\nReceived keyboard interrupt, shutting down...")
    finally:
        for p, name in [(process1, "Process 1"), (process2, "Process 2")]:
            if p.is_alive():
                p.terminate()
                print(f"{name} terminated.")
                p.join()
        print("System is terminated.")