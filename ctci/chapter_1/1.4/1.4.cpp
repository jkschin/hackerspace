#include <map>
#include <assert.h>
#include <iostream>

using namespace std;

bool IsPalindrome(string str) {
  map<char, int> counts;
  int total_chars = 0;
  for (char& c : str) {
    c = tolower(c);
    if (c != ' ') {
      counts[c]++;
      total_chars++;
    }
  }
  int num_odd = 0;
  int num_even = 0;
  for (auto const& x : counts) {
    char c = x.first;
    if (counts[c] % 2 == 0) {
      num_even++;
    }
    else {
      num_odd++;
    }
  }
  if (total_chars % 2 == 0) {
    if (num_odd > 1) {
      return false;
    }
    else {
      return true;
    }
  }
  else {
    if (num_odd > 1) {
      return false;
    }
    else {
      return true;
    }
  }
}

int main() {
  assert(IsPalindrome("AAABBBCCCCDDDD") == false);
  assert(IsPalindrome("AAABBBCCCC") == false);
  assert(IsPalindrome("AAABBBCCC") == false);
  assert(IsPalindrome("AAABBCCC") == false);
  assert(IsPalindrome("AAABBAAA") == true);
  assert(IsPalindrome("AABBCCDEF") == false);
  assert(IsPalindrome("aa BBc CDEF   ") == false);
  cout << "All Tests Passed!" << endl;
}
