#from itertools import count
from math import log
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
    return (int)(abs((hashCount*dictSize)/log(1-falsePositiveRate**(1/hashCount))))

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
            
            bloom5[md5 % len(bloom5)] = True
            bloom5[sha224 % len(bloom5)] = True
            bloom5[sha256 % len(bloom5)] = True
            bloom5[sha384 % len(bloom5)] = True
            bloom5[sha512 % len(bloom5)] = True

def testInputPasswords(input, bloom3, bloom5):
    md5, sha224, sha256, sha384, sha512 = 0, 0, 0, 0, 0
    bf3Results = []
    bf5Results = []
    bool3, bool5 = True, True
    with open(input, 'r') as f:
        for line in f:
            line = line.strip()
            line = line.encode('utf-8')
            md5, sha224, sha256, sha384, sha512 = hashInputLine(line, md5, sha224, sha256, sha384, sha512)
            
            if (bloom3[md5 % len(bloom3)] == False) or (bloom3[sha384 % len(bloom3)] == False) or (bloom3[sha512 % len(bloom3)] == False):
                bool3 = False
            
            if (bloom5[md5 % len(bloom5)] == False) or (bloom5[sha224 % len(bloom5)] == False) or (bloom5[sha256 % len(bloom5)] == False) or (bloom5[sha384 % len(bloom5)] == False) or (bloom5[sha512 % len(bloom5)] == False):
                bool5 = False
            bf3Results.append(bool3)
            bf5Results.append(bool5)
    return bf3Results, bf5Results

def writeOutput(results, output):
    with open(output, 'w') as f:
        for i in range(len(results)):
            if results[i] == True:
                f.write('Maybe\n')
            else:
                f.write('No\n')
            
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
    print('Writing Bloom3 results to file...')
    writeOutput(bf3Results, args.output3)
    print('Writing Bloom5 results to file...')
    writeOutput(bf5Results, args.output5)

    print('Done')

if __name__ == '__main__':
    main()