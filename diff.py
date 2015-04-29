def Wagner_Fischer(in_string, out_string):
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
                    d[i-1][j] + 1,      # deletion of a character
                    d[i][j-1] + 1,      # insertion of a character
                    d[i-1][j-1] + 1     # substitution of a character
                    )

    return d[-1][-1]

# Wagner_Fischer("aebc","abde") == 3
# Wagner_Fischer([1,2,3],[1,2,3,4]) == 1
# Wagner_Fischer([1,2,3],[1,2,4,4]) == 2