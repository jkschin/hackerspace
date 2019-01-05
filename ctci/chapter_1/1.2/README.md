The question is to find out if 2 strings are permutations of each other. If they
aren't of equal length, they are definitely not permutations so that should be
the first check. 

If they are of equal length **and** both are sorted, then the simplest solution
is to compare each character in the same index. The termination condition would
be when there's not a match or when everything matches. The time complexity of
this is `O(n)` and `O(1)`. Of course, it is probably not going to be that
simple.

If they are of equal length **and** not sorted, then the brute force solution
would be to compare the first character in `str1` and all characters in `str2`.
If there's a match, remove it from `str2`. Move on to the next character in
`str1` and repeat. The termination condition would be when a character in `str1`
can't be found in `str2`, thus returning `false` or when every character in
`str1` can be found in `str2`, thus returning `true`. The time complexity of
this is `O(n**2)` and space complexity is `O(1)`.

A smarter solution would be to sort both strings, incurring a time cost of `O(n
log(n))` on both strings, and then doing the comparison as if it were sorted.
The space complexity is not constant, depending on the sort implementation. It's
definitely not `O(1)` and it's probably going to be around `O(n)`. Can we do
better?

The better solution would be to use an `unordered_map` to add each character and
the respective counts for `str1`, and then once that's complete, subtract the
counts for each character using `str2`. The time complexity is `O(n)` and the
space complexity is `O(n)`. Of course space complexity is based on cardinality
but we can just approximate `O(n)`.
