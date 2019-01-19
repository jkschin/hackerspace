The function is supposed to return a boolean value instead of all possible
permutations of the string. In the examples given, they do not have to be
dictionary words and spaces do not count.

Breakdown of a Palindrome:
1. Can have both even and odd number of characters.
2. If odd, only one character can have an odd count. For example, "aaa" and the
   rest of the count of the characters have to be even. "bb", "cc", "dd". When
   you have "aaa" and "eee", it's impossible as you cannot choose a centre point
   to pivot.
3. If even, all characters have to have an even count, as the pivot point will
   be the same characters. For example, if there are 3 characters "aaa", they
   can't be placed in the middle as 1 more or less "a" is required.

Other Considerations:
1. There can be upper and lower case characters. Be sure to lower case
   everything.
2. Ignore spaces.
3. Assume 26 characters of the alphabet.

One solution is to use an unordered map as we do not need the characters to be
ordered. In any case, the cardinality of the map is only 26 so the performance
of these 2 is probably not going to be significant.

Pseudo Code:
1. Start with first character of string.
2. If valid character, add to map. Else, ignore. Increase total_chars count.
3. Repeat till map is built.
4. Traverse map. If total_chars is odd, flag when we see an odd count and return
   false when we see another odd count, else return true. If total_chars is
   even, return false when we see an odd count, else return true.

Test Cases:
1. AAABBBCCCCDDDD - False
2. AAABBBCCCC -False 
3. AAABBBCCC - False
4. AAABBCCC - False
5. AAABBAAA - True
6. AABBCCDEF - False

