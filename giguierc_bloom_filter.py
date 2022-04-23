#from itertools import count
import time # not needed for program. Used for timing bloom3 vs bloom5
import math
from math import log
import hashlib
import argparse
from bitarray import bitarray

falsePositiveRate = 0.0001
#falsePositiveRate = 0.01 # Desired false positive rate, default 0.01
# This is used in calculating the size of the bloom filters
    
def countDictSize(dictionary):
    count = 0
    with open(dictionary, 'r') as f:
        for line in f:
            count += 1
    return count

def calculateArraySize(dictSize, hashCount):
    return int(dictSize * log(2) / (log(2) ** hashCount * falsePositiveRate))

    # Source for formula: GeeksforGeeks
    # https://www.geeksforgeeks.org/bloom-filters-introduction-and-python-implementation/
    #return int(abs((dictSize * log(falsePositiveRate)) / (log(2)) ** 2))
    
    #return (int)(abs((hashCount*dictSize)/log(1-falsePositiveRate**(1/hashCount))))

def fillBloomFilters(bloom3, bloom5, dictionary):
    with open(dictionary, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.encode('utf-8')

def hashInputLine(line, md5, sha224, sha256, sha384, sha512):
    
    md5 = int(hashlib.md5(line).hexdigest(), 16)
    sha224 = int(hashlib.sha224(line).hexdigest(), 16)
    sha256 = int(hashlib.sha256(line).hexdigest(), 16)
    sha384 = int(hashlib.sha384(line).hexdigest(), 16)
    sha512 = int(hashlib.sha512(line).hexdigest(), 16)

    return md5, sha224, sha256, sha384, sha512

def hashDictionary(dictionary, bloom3, bloom5):
    md5, sha224, sha256, sha384, sha512 = 0, 0, 0, 0, 0
    with open(dictionary, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.encode('utf-8')
            md5, sha224, sha256, sha384, sha512 = hashInputLine(line, md5, sha224, sha256, sha384, sha512)
            
            bloom3[md5 % len(bloom3)] = True
            bloom3[sha384 % len(bloom3)] = True
            bloom3[sha512 % len(bloom3)] = True
            bloom3End = time.perf_counter()
            
            bloom5[md5 % len(bloom5)] = True
            bloom5[sha224 % len(bloom5)] = True
            bloom5[sha256 % len(bloom5)] = True
            bloom5[sha384 % len(bloom5)] = True
            bloom5[sha512 % len(bloom5)] = True

def testInputPasswords(input, bloom3, bloom5):
    print('entered testInputPasswords')
    md5, sha224, sha256, sha384, sha512 = 0, 0, 0, 0, 0
    bf3Results = []
    bf5Results = []
    bool3, bool5 = True, True
    f = open(input, 'r')
    next(f)
    for line in f:
        line = line.strip()
        line = line.encode('utf-8')
        md5, sha224, sha256, sha384, sha512 = hashInputLine(line, md5, sha224, sha256, sha384, sha512)   


        #bloom3Start = time.perf_counter()
        if (bloom3[md5 % len(bloom3)] == False) or (bloom3[sha384 % len(bloom3)] == False) or (bloom3[sha512 % len(bloom3)] == False):
            bool3 = False
        #bloom3End = time.perf_counter()
        
        #bloom5start = time.perf_counter()
        if (bloom5[md5 % len(bloom5)] == False) or (bloom5[sha224 % len(bloom5)] == False) or (bloom5[sha256 % len(bloom5)] == False) or (bloom5[sha384 % len(bloom5)] == False) or (bloom5[sha512 % len(bloom5)] == False):
            bool5 = False
        #bloom5End = time.perf_counter()
        
        bf3Results.append(bool3)
        bf5Results.append(bool5)
        

        #bloom3Time = bloom3End - bloom3Start
        #bloom5Time = bloom5End - bloom5start
        
        #print(f"bloom3Time: {bloom3Time:0.10f}")
        #print(f"bloom5Time: {bloom5Time:0.10f}")

    return bf3Results, bf5Results

def writeOutput(results, output, input):
    i = open(input, 'r')
    inputs = i.readlines()[1:]
    with open(output, 'w') as f:
        for i in range(len(results)):
            outputString = str(inputs[i].strip('\n')) + ' '
            if results[i] == True:
                outputString += 'maybe\n'
                f.write(outputString)
            else:
                outputString += 'no\n'
                f.write(outputString)

def falsePosProb(hashCount, dictSize, arraySize):
    return (1 - (1 - (1/arraySize)) **(hashCount * dictSize)) ** hashCount


def main():
    parser = argparse.ArgumentParser(description='Bloom Filter')
    parser.add_argument('-d', action='store', default='dictionary.txt', dest='dictionary')
    parser.add_argument('-i', action='store', default='input.txt', dest='input')
    parser.add_argument('-o3', action='store', default='output3.txt', dest='output3')
    parser.add_argument('-o5', action='store', default='output5.txt', dest='output5')
    args = parser.parse_args()

    # Read dictionary
    print('Reading dictionary...')
    dictSize = countDictSize(args.dictionary)
    print('Dictionary size:', dictSize, 'entries')
    bloom3Size = calculateArraySize(dictSize, 3)
    bloom5Size = calculateArraySize(dictSize, 5)
    print('Bloom filter sizes: Bloom3:', bloom3Size, ', Bloom5:', bloom5Size)

    # Create bloom filters
    print('Creating bloom filters...')
    bloom3 = bitarray(bloom3Size)
    bloom5 = bitarray(bloom5Size)
    
    # Initialize bloom filters to all zeroes
    bloom3.setall(False)
    bloom5.setall(False)
    print('Bloom filters initialized')

    # Hash dictionary
    print('Hashing dictionary...')
    hashDictionary(args.dictionary, bloom3, bloom5)

    # Test input passwords
    print('Testing input passwords...')
    bf3Results, bf5Results = testInputPasswords(args.input, bloom3, bloom5)

    # Write results to file
    print('Writing Bloom3 results to', args.output3, '...')
    writeOutput(bf3Results, args.output3, args.input)
    print('Writing Bloom5 results to', args.output5, '...')
    writeOutput(bf5Results, args.output5, args.input)

    # Calculate false positive probabilities
    print('Calculating false positive probabilities...')
    bf3FalsePosProb = falsePosProb(3, dictSize, bloom3Size)
    bf5FalsePosProb = falsePosProb(5, dictSize, bloom5Size)
    print('Bloom3 false positive probability:', bf3FalsePosProb)
    print('Bloom5 false positive probability:', bf5FalsePosProb)
    bf5DifferentSize = falsePosProb(5, dictSize, bloom3Size)
    print('Bloom5 false positive probability with Bloom3 size:', bf5DifferentSize)

    print('Done')

if __name__ == '__main__':
    main()