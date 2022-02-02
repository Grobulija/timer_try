import logging
from timer import Timer
from sorts import bubble_sort, merge_sort
import numpy as np


@Timer(name="decorator_block", format='{D}d {H}h {M:02}m {S:02}s {MS:03}ms')
def selection_sort(nums):
    for i in range(len(nums)):
        lowest_value_index = i
        for j in range(i + 1, len(nums)):
            if nums[j] < nums[lowest_value_index]:
                lowest_value_index = j
        nums[i], nums[lowest_value_index] = nums[lowest_value_index], nums[i]


if __name__ == '__main__':
    A = np.random.randint(0, 100, size=30000).reshape(10, 3000)

    selection_sort(A[7])

    with Timer(format='{H}h {S}s {MS:03}ms'):
        bubble_sort(A[0])

        with Timer(name="A block", format='{H}h {MS:03}ms'):
            merge_sort(A[1])

            with Timer(name="B block"):
                merge_sort(A[2])

    with Timer(name="C block"):
        with Timer():
            merge_sort(A[3])

        merge_sort(A[4])

        with Timer():
            merge_sort(A[5])

    t = Timer(name="class block")
    t.start()
    merge_sort(A[6])
    t.stop()
    Timer.get_order()
