def minimumSwaps(arr):
    sorted_arr = sorted(arr)
    idx = [i for i in range(len(arr))]
    dic = dict(zip(sorted_arr, idx))
    arr = [dic[i] for i in arr]
    print arr
    i = 0
    swaps = 0
    while i < (len(arr)):
        if arr[i] != i:
            arr[arr[i]], arr[i] = arr[i], arr[arr[i]]
            swaps += 1
        else:
            i += 1
    return swaps

print minimumSwaps([1,3,5,2,4,6,8])
