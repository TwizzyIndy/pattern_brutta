#############
#
#
# Coded by TwizzyIndy
#
#
# Pattern Brutta
#
# Android pattern lock bruteforce script
#
# REF: http://forensics.spreitzenbarth.de/2012/02/28/cracking-the-pattern-lock-on-android/
#
# Twitter : @TwizzyIndy
#
#
#############

import os
import sys
import time
import multiprocessing
import hashlib
import binascii
import itertools

MATRIX_SIZE = [3,3]
MAX_LEN = MATRIX_SIZE[0]*MATRIX_SIZE[1]
FOUND = multiprocessing.Event()

def lookup(param):
    global FOUND
    lenhash = param[0]
    target = param[1]
    positions = param[2]

    if FOUND.is_set() is True:
        return None


    permutations = itertools.permutations(positions, lenhash)

    for item in permutations:
        
        if FOUND.is_set() is True:
            return None
        pattern = ''.join(str(v) for v in item)

        # convert the pattern to hex (so the string '123' becomes '\x01\x02\x03')
        key = binascii.unhexlify(''.join('%02x' % (ord(c) - ord('0')) for c in pattern))

        # calculating hash
        sha1 = hashlib.sha1(key).hexdigest()

        # its found
        if sha1 == target:
            FOUND.set()
            return pattern

    # its not found
    return None

def brutta(myhash):
    ncores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(ncores)
    # generates the matrix positions IDs
    positions = []
    for i in range(0,MAX_LEN):
        positions.append(i)
    
    # sets the length for each worker
    params = []
    count = 1
    for i in range(0,MAX_LEN):
        params.append([count,myhash,positions])
        count += 1
    
    result = pool.map(lookup,params)
    pool.close()
    pool.join()
    
    ret = None
    for r in result:
        if r is not None:
            ret = r
            break
    return ret

def main():
    print ''

    print '[* Pattern Brutta      *]'
    print ''

    print '[* Coder : TwizzyIndy  *]'
    print '[* Twitter: @TwizzyIndy*]'

    print ''
    
    print 'REF: http://forensics.spreitzenbarth.de/2012/02/28/cracking-the-pattern-lock-on-android/\n'
    
    # check parameters
    if len(sys.argv) != 2:
        print 'Usage: python %s gesture.key\n' % sys.argv[0]
        sys.exit(0)
    
    # check gesture.key file
    if not os.path.isfile(sys.argv[1]):
        print "Access to %s is failed\n" % sys.argv[1]
        sys.exit(-1)
        
    # load SHA1 hash from file
    f = open(sys.argv[1], 'rb')
    gest = f.read(hashlib.sha1().digest_size).encode('hex')
    f.close()

    # check hash length
    if len(gest) / 2 != hashlib.sha1().digest_size:
        print "I can work with this type of file..\n"
        sys.exit(-2)

    # its time to bruteforce the pattern !

    pattern = brutta(gest)

    if pattern is None:
        print "Sorry I cant calculate ..."
        rcode = -1
    else:
        print "Your pattern is %s\n" % pattern
        print ""
        
        print "Guide to reading :\n"
        print "[0]  [1]  [2] "
        print "[3]  [4]  [5] "
        print "[6]  [7]  [8] \n"
        rcode = 0

    sys.exit(rcode)

if __name__ == "__main__":
    main()
