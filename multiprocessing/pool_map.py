import multiprocessing
import time


def count(n):
    c = 0
    for i in range(n):
        c += 1
    assert c == n


if __name__ == "__main__":
    cases = [i*1000000 for i in range(10)]

    start_time = time.time()
    for case in cases:
        count(case)
    end_time = time.time()
    print(f"without pool: {end_time - start_time}")

    start_time = time.time()
    pool = multiprocessing.Pool(processes=4)
    pool.map(count, cases)
    end_time = time.time()
    print(f"with pool: {end_time - start_time}")
