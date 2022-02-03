import time
import multiprocessing

if __name__ == "__main__":

    start = time.perf_counter()

    def do_sth():
        print("Sleeping 1 second...")
        time.sleep(1)
        print("Done sleeping")

    p1 = multiprocessing.Process(target=do_sth)
    p2 = multiprocessing.Process(target=do_sth)

    # p1.start()
    # p2.start()

    # p1.join()
    # p2.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish-start, 2)} second(s)")