#include <string>
#include <iostream>

using namespace std;

void URLify(string* p_str, string rep, int true_length) {
  string& str = *p_str;
  int p1 = true_length - 1;
  int p2 = str.length() - 1;
  while (p1 != 0 && p2 != 0) {
    if (str[p1] != ' ' ) {
      str[p2] = str[p1];
      --p2;
    }
    else {
      for (int i = rep.length() - 1; i >= 0; --i) {
        str[p2] = rep[i];
        --p2;
      }
    }
    --p1;
  }
}

int main() {
  string str = "Mr John Smith    ";
  string rep = "%20";
  int true_length = 13;
  URLify(&str, rep, true_length);
  cout << str << endl;
}


