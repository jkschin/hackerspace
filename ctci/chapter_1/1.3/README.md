First thought was to iterate through the list from left to right. Whenever I
encounter a space, start writing `%20` in write out the existing characters to
temporary variables. As I was doing this, I realized that this isn't a great
idea as if the characters to be replaced are longer, then the memory
requirements would be higher. In addition, every insertion would require
shifting the entire string down and thus in the worst case of everything being a
space, the complexity would be approximately `O(n^2)` where `n` is the length of
the string. 

This solution does not require using the length of the real string, so that's
where the catch is. What if I started from the right instead? All the empty
characters are already on the right. I can simply have 2 pointers and shift them
downwards. No extra memory is needed in this case and the algorithm runs in
`O(n)`.
