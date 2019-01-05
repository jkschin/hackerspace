#include <string>
#include <unordered_map>
#include <iostream>
using namespace std;

bool isPermutation (string str1, string str2) {
  unordered_map<char,int> my_map;
  unordered_map<char,int>::iterator it;
  if (str1.length() != str2.length()) return false;
  for (const char &c: str1) {
    my_map[c]++;
  }
  for (const char &c: str2) {
    my_map[c]--;
    if (my_map[c] == 0) {
      my_map.erase(c);
    }
  }
  if (my_map.size() == 0) {
    return true;
  }
  else {
    return false;
  }
}

int main() {
  // return true
  string str1_1 = "ABCDE";
  string str1_2 = "EDABC";
  cout << isPermutation(str1_1, str1_2) << endl;

  // return false
  string str2_1 = "ABCDE";
  string str2_2 = "ABCEE";
  cout << isPermutation(str2_1, str2_2) << endl;

  // return false
  string str3_1 = "ABCDE";
  string str3_2 = "ABCDEE";
  cout << isPermutation(str3_1, str3_2) << endl;
}
