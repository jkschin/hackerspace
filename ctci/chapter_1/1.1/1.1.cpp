#include <string>
#include <iostream>
#include <set>
#include <typeinfo>
#include <algorithm>
#include <vector>

using namespace std;

bool isUnique(string str) {
  set<char> my_set;
  for (unsigned int i = 0; i < str.size(); ++i) {
    if(my_set.find(str[i]) == my_set.end()) {
      my_set.insert(str[i]);
    }
    else {
      return false;
    }
  }
  return true;
}

bool isUnique2(string str) {
  string::iterator it;
  sort(str.begin(), str.end());
  it = adjacent_find(str.begin(), str.end());
  if (it == str.end()) {
    return false;
  }
  else {
    return true;
  }
}

int main()
{
  const string str1 = "EABCDE";
  const string str2 = "ABCDEFGH";
  bool ans1 = isUnique2(str1);
  bool ans2 = isUnique2(str2);
  cout << ans1 << endl;
  cout << ans2 << endl;
}
