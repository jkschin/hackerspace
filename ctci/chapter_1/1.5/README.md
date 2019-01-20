The function is supposed to return a boolean value. True if the 2 strings have
an edit distance of 1 or less, false otherwise. 

Assumptions:
1. Only small letters, no spaces, and the 26 letters of the alphabet.
2. No idea of the length of both strings a priori. 

Test Cases:
1. aabb abb - True
2. aabb aab - True
3. aabb bbc - False
4. aabb abc - False
5. aabb aaab - True
6. aabb aaa - False
7. aabc aac - True
8. abcd bcd - True

Cases 5 and 7 are the most interesting, as one is a replace and the other is a
delete. 


**Case 5 Walkthrough - Replace**

```
**Not Equal**
a a b b 
    ^ 

a a a b
    ^

**Not Equal**
a a b b 
      ^

a a a b
    ^

**Equal**
a a b b 
      ^

a a a b
      ^ 
```

**Case 7 Walkthrough - Deletion**

```
**Not Equal**
a a b c
    ^

a a c
    ^

**Equal**
a a b c
      ^ 

a a c
    ^
```

Pseudo Code:
1. Start with first character of both strings.
2. If equal:
  1. Increment both pointers.
  2. Continue checking the next characters the pointers are pointing to.
3. Else:
  1. If first_string:
      1. Increment first string by 1.
      2. first_string = false.
      3. edits++;
  2. Else:
      1. Increment second string by 1.
      2. first_string = true.
4. If edits > 1:
  1. return false
5. return true at the end of the for loop

Turns out that this pseudo code does not really work and it overcomplicates
matters. I'm just leaving this out there and not editing it. The code itself
does not work in this way as what I initially wrote failed one of the test
cases and I changed the code immediately.

After writing the new code, I realized I forgot one extra test case. I assumed
that `str1` will always be longer than `str2`. That however may not be true. I
added another `else if` to catch that and that test passed after too.

This problem is constrained as we only have to catch a case where the edit
distance is greater than 1. I was reading up more on this and found the general
case of minimum edit distance. That would involve dynamic programming and is
more complicated than this.
