import timeit

key = (
'01001010101010100111010101101100010010100101001010101010101000101011'
'01001010101010100111010101101100010010100101001010101010101000101011'
'01001010101010100111010101101100010010100101001010101010101000101011'
'01001010101010100111010101101100010010100101001010101010101000101011'
'01001010101010100111010101101100010010100101001010101010101000101011'
)
key = int(key, 2)

def wrapper(func, key):
    def wrapped():
        return func(key)
    return wrapped

def count(key):
    return bin(key)[2:].count('1')

def count2(key):
    count = 0
    for c in bin(key)[2:]:
        if c == '1':
            count += 1
    return count

def count3(key):
    count = 0
    while key != 0:
        count += (key & 1)
        key = key >> 1
    return count

# 9999 because this is ridiculously long.
def count9999(key):
    return sum([int(z) for z in list(bin(key)[2:])])

print count(key)
print count2(key)
print count3(key)
print count9999(key)
print timeit.timeit(wrapper(count, key), number=10000)
print timeit.timeit(wrapper(count2, key), number=10000)
print timeit.timeit(wrapper(count3, key), number=10000)
print timeit.timeit(wrapper(count9999, key), number=10000)
