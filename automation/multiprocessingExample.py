import time
import multiprocessing
import concurrent.futures
from tqdm import tqdm


def do_sth(seconds):
    print(f"Sleeping {seconds} second(s)...")
    time.sleep(seconds)
    return f"Done sleeping {seconds}"


if __name__ == "__main__":

    start = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        results = executor.map(do_sth, secs)

        for result in results:
            print(result)

        # results = [executor.submit(do_sth, sec) for sec in secs]
        # for f in concurrent.futures.as_completed(results):
        #     print(f.result())

    finish = time.perf_counter()

    print(f"Finished in {round(finish - start, 2)} second(s)")
