from itertools import count
import math
import hashlib
import argparse
from bitarray import bitarray

falsePositiveRate = 0.01

def countDictSize(dictionary):
    count = 0
    with open(dictionary, 'r') as f:
        for line in f:
            count += 1
    return count

def calculateArraySize(dictSize, hashCount):
    return int(math.ceil(dictSize * math.log(2) / math.log(1 / falsePositiveRate) / hashCount))

def fillBloomFilters(bloom3, bloom5, dictionary):
    with open(dictionary, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.encode('utf-8')
            

def main():
    parser = argparse.ArgumentParser(description='Bloom Filter')
    parser.add_argument('-d', action='store', default='dictionary.txt', dest='dictionary')
    parser.add_argument('-i', action='store', default='input.txt', dest='input')
    parser.add_argument('-o3', action='store', default='output3.txt', dest='output3')
    parser.add_argument('-o5', action='store', default='output5.txt', dest='output5')
    args = parser.parse_args()

    # Read dictionary
    dictSize = countDictSize(args.dictionary)
    print('Dictionary size:', dictSize)
    bloom3Size = calculateArraySize(dictSize, 3)
    bloom5Size = calculateArraySize(dictSize, 5)
    print('Bloom filter size:', bloom3Size, bloom5Size)

    # Create bloom filters
    bloom3 = bitarray(bloom3Size)
    bloom5 = bitarray(bloom5Size)
    # Initialize bloom filters to all zeroes
    bloom3.setall(False)
    bloom5.setall(False)




if __name__ == '__main__':
    main()