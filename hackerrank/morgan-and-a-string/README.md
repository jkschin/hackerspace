An expert level HackerRank question. Definitely worth giving this problem a
shot. A maximum of 5 test cases will be in a set.

Input:
2 Strings. Only capital letters. String 1 can be longer than String 2. Each
string has a maximum length of `10^5`. 

Output:
The lexicographically minimal string for each test case in a new line.

Breakdown of Lexicographically Minimal String:
Each character can be assigned a number. For example, A to 0, B to 1, etc. Given
`ACABCF` as a character set, the lexigographical minimal string would be
`AABCCF`. However, this is not what the question is asking, as there is an
additional constraint. The characters `ACA` and `BCF` are broken up into 2
stacks, and you can only take a letter when it's at the top of the list. Simply
concatenating both and then sorting it would not be a solution (assuming this is
optimal in the first place). The answer to this scenario is thus `ABCACF`. The
prompt was kind enough to mention how ties are resolved.

Analysis:
Off the top of my head, it seems like a fairly simple problem but on digging
deeper, there is actually a catch in extremely long ties. For example:

`AACCCCCCCCCCCCCCCCD`
`BBCCCCCCCCCCCCCCCCE`

The greedy solution that I thought of after seeing the prompt would be to look
ahead. However, the worst case of looking ahead here would be till the end of
the string. And what if the look ahead was always repeated? For example:

`AACCCACCCACCCACCCACCCA`
`BBCCCECCCECCCECCCECCCE`

The first part of the string is `AABBCCCA`. We have look at all the ties up to
the point where it is differentiated because we have to pop from a certain
stack.

a = `CCCACCCACCCACCCA`
b = `CCCECCCECCCECCCECCCE`
result = `AABBCCCA`

At this stage `CCCA` has to be selected again and you only know that after
stepping through all the `C`s. This will continue until `a` is empty and then
`b` can simple be concatenated.

I thought these are the cases that I did not cover, until I saw the example:

a = `ABACABA`
b = `ABACABA`

What if they are identical? The method I described above would trace all the way
till the end and then simply concatenate both. This is not right.

The solution is simple when there are no ties. When there are ties, the question
that the algorithm should ask would be is there something ahead that is better
than the current tie? For example, given `BA` and `BA`, `A` is better than `B`
and thus the answer is `BABA`. Yet, if given `BC` and `BC`, `C` is worse than
`B` and thus the answer is `BBCC`.

Pseudo Code:
1. Start with the first characters of each string.
2. Look ahead.
  1. a smaller
    1. Pop from string a.
  2. b smaller
    2. Pop from string b.
  3. Tie 
    0. If reference character not null and current character is larger:
      1. Terminate.
    1. Else If both string a and b have next characters.
      1. Look ahead. Pass current character as reference character.
    2. Else
      1. If string a next character is end of list. Pop from string a.
      2. If string b next character is end of list. Pop from string b.

From the pseudo code, this is starting to look like a recursion.

