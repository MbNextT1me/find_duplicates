import os
import time
import random


def generate_R_table():
    R_table = {}
    n = 256  # number of ascii characters
    nums = [i for i in range(10 ** 5)]
    for i in range(n):
        value = random.randint(0, len(nums)-1)
        R_table[i] = nums[value]
        nums.pop(value)
    return R_table


def find_duplicates(files: list[str], hash_function: callable) -> list[str]:
    start_time = time.time()
    list_uniq = set()
    for i in files:
        list_uniq.add(hash_function(i))
    print("--- %s seconds ---" % (time.time() - start_time))
    return list(list_uniq)


def CRC(file):
    h = 0
    for i in range(len(file)):
        ki = ord(file[i])
        highorder = h & 0xf8000000
        h = h << 5
        h = h ^ (highorder >> 27)
        h = h ^ ki
    return h


def PJW(file):
    h = 0
    for i in range(len(file)):
        ki = ord(file[i])
        h = (h << 4) + ki
        g = h & 0xf0000000
        if g != 0:
            h = h ^ (g >> 24)
            h = h ^ g
    return h


def BUZ(file):
    h = 0
    for i in range(len(file)):
        ki = ord(file[i])
        highorder = h & 0x80000000
        h = h << 1
        h = h ^ (highorder >> 31)
        h = h ^ R[ki]
    return h


def read_all_files(dir_path: str):
    files = []
    for filename in os.listdir(dir_path):
        with open(os.path.join(dir_path, filename), 'r') as f:
            lines = f.read()
            files.append("".join(lines.split()))
    return files


path = "out"
arr = read_all_files(path)
R = generate_R_table()

print("CRC time")
arr_with_out_dupl = find_duplicates(arr, CRC)
print("Amount of dupl: ", len(arr)-len(arr_with_out_dupl), "\n")

print("PJW time")
arr_with_out_dupl = find_duplicates(arr, PJW)
print("Amount of dupl: ", len(arr)-len(arr_with_out_dupl), "\n")

print("BUZ time")
arr_with_out_dupl = find_duplicates(arr, BUZ)
print("Amount of dupl: ", len(arr)-len(arr_with_out_dupl))
