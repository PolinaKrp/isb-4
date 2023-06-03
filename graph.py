import multiprocessing as mp
import time

import matplotlib.pyplot as plt
import numpy as np

from hashing import check_hash


def graph_drawing(card: str) -> None:
    """
    Graph drawing function
    """
    times = np.empty(shape=0)
    card = card[:6]
    items = [(i, card) for i in range(99999, 10000000)]
    for i in range(1, 8):
        start = time.time()
        with mp.Pool(i) as p:
            for i, result in enumerate(p.starmap(check_hash, items)):
                if result:
                    end = time.time() - start
                    times = np.append(times, end)
                    break
    plt.plot(range(len(times)), np.round(times, 2).tolist())
    plt.xlabel("Size pool")
    plt.ylabel("Time in seconds")
    plt.show()