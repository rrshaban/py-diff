import time

def Wagner_Fischer(in_string, out_string, 
    insertion_cost=1, deletion_cost=1, substitution_cost=2):
    # Will produce a matrix of edit distances such that d[i,j] is the 
    # Levenshtein difference between in_string[:i] and out_string[:j]. These 
    # i and j are 1-indexed, as the Wagner-Fischer algorithm requires an 
    # empty first row and column to allow for insertion of a new character.

    # Initialize empty array
    d = list()

    for i in range(len(in_string)+1):
        # distance between empty zero-length string and in_string[:i]
        d.append([i]+[0]*(len(out_string)))

    for j in range(len(out_string)+1):
        # distance between empty zero-length string and out_string[:i]
        d[0][j] = int(j)

    for i in range(1, len(in_string)+1):
        for j in range(1, len(out_string)+1):

            if in_string[i-1] == out_string[j-1]:
                # No edit required, these extensions of the string are the same
                d[i][j] = d[i-1][j-1]
            else:
                d[i][j] = min(
                    d[i-1][j] + deletion_cost,      # deletion of a character
                    d[i][j-1] + insertion_cost,     # insertion of a character
                    d[i-1][j-1] + substitution_cost # substitution of a character
                    )

    return d[-1][-1] # Levenshtein edit distance for in_string -> out_string

def Myers(a, b):
    m, n = len(a), len(b)

    if m > n:
        # if in string is longer than out string, swap their positions
        a, b = b, a
        m, n = n, m

    def snake(k, y):
        # snakes across the diagonal as long as a[x] and b[y] are identical
        x = y - k

        # these counts differ from the algorithm because of zero-counting
        while (x < m) and (y < n) and (a[x] == b[y]):
            x += 1
            y += 1
        return y


    offset = m + 1
    delta = n - m   # delta is the difference in length between the two arrays
    size = m + n + 3
    
    fp = [-1]*size
    p = -1

    while True:
        p += 1

        # iterate from -p through delta
        for k in range(-p, delta, 1):
            #   len(fp), (k, offset)
            fp[k + offset] = snake(k, max(fp[k - 1 + offset] + 1, 
                                          fp[k + 1 + offset]    ))

        # iterate backwards from p + delta down to delta
        for k in range(delta + p, delta, -1):
            fp[k + offset] = snake(k, max(fp[k - 1 + offset] + 1, 
                                          fp[k + 1 + offset]    ))

        fp[delta + offset] = snake(delta, max(fp[delta - 1 + offset] + 1,
                                              fp[delta + 1 + offset]    ))

        if fp[delta + offset] >= n: 
            return delta + (2 * p)

def test(fun):
    # speed test texts from Google's Neil Fraser
    # https://code.google.com/p/google-diff-match-patch/
    # Set up as a character-by-character diff, so much slower and more precise
    text1 = open("speedtest1.txt").readlines()
    text2 = open("speedtest2.txt").readlines()

    start_time = time.time()

    # Google test suite and trivial examples
    fun(text1, text2)
    fun("abc", "xyz")
    fun("1234abcdef", "1234xyz")
    fun("1234", "1234xyz")
    fun("abc", "xyz")
    fun("abcdef1234", "xyz1234")
    fun("1234", "xyz1234")
    fun("", "abcd")
    fun("abc", "abcd")
    fun("123456xxx", "xxxabcd")

    end_time = time.time()

    print "Google test suite elapsed time: {0}".format(end_time - start_time)

    # Identical file
    start_time = time.time()
    fun(text1, text1)
    end_time = time.time()
    print "Identical file elapsed time: {0}".format(end_time - start_time)
    
    text1 = open("plot1000").readlines()
    text2 = open("plot6000").readlines()

    # Large, effectively random and dissimilar files

    start_time = time.time()
    fun(text1, text2)
    end_time = time.time()
    print "Large random data elapsed time: {0}".format(end_time - start_time)


def main():
    
    print "Wagner_Fischer testing:"
    test(Wagner_Fischer)
    print "Myers testing:"
    test(Myers)


main()










