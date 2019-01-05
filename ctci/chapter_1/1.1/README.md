A really simple problem. Writing it in C++ to get familiar with it again and
make C++ my go-to language. I only wrote 2 test cases for this and had to
compile the code twice just to test it. There has to be a better way to do this.

The time complexity is `O(n)`, where `n` is the length of the string and you
only have to iterate through it once. The space complexity is `O(m)`, where
`m` is the cardinality of the set. In this case, we can assume `m` to be 54, the
total number of upper and lower case characters. At worst, the cardinality is
`n` and we can assume space complexity to be `O(n)` for simplicity.

The prompt suggests that you can do it without additional data structures.
Assuming it's the ASCII character set, each character can be converted into an
integer. If the list already comes sorted, then we can just compare the
adjacent elements in place and achieve `O(n)` time complexity and `O(1)` space
complexity. If it doesn't, we can do a sort in `O(n log(n))` and then it is the
same as if it was sorted.
