#include <string>
#include <iostream>
#include <assert.h>

using namespace std;

bool IsOneAway(string str1, string str2) {
  string::iterator it1 = str1.begin();
  string::iterator it2 = str2.begin();
  int edits = 0;
  while(it1 != str1.end() && it2 != str2.end()) {
    if (*it1 == *it2) {
      ++it1;
      ++it2;
    }
    else {
      // This is an insertion or deletion.
      if (*(it1 + 1) == *it2) {
        ++it1;
      }
      else if (*(it1) == *(it2 + 1)) {
        ++it2;
      }
      // This is a substitution. 
      else if (*(it1 + 1) == *(it2 + 1)) {
        ++it1;
        ++it2;
      }
      ++edits;
    }
    if (edits > 1) {
      return false;
    }
  }
  return true;
}

int main() {
  assert(IsOneAway("aabb", "abb") == true);
  assert(IsOneAway("aabb", "aab") == true);
  assert(IsOneAway("aabb", "bbc") == false);
  assert(IsOneAway("aabb", "abc") == false);
  assert(IsOneAway("aabb", "aaab") == true);
  assert(IsOneAway("aabb", "aaa") == false);
  assert(IsOneAway("aabc", "aac") == true);
  assert(IsOneAway("abcd", "bcd") == true);
  assert(IsOneAway("bcd", "abcd") == true);
  cout << "All Tests Passed!" << endl;
}
