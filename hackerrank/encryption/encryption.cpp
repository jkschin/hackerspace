#include <fstream>
#include <iostream>
#include <math.h>
#include <vector>

using namespace std;

typedef vector<char> vc;
typedef vector<vector<char>> vvc;

// Complete the encryption function below.
string encryption(string s) {
  int len = s.length();
  int r = floor(sqrt(len));
  int c;
  cout << r << endl;
  if (r * r >= len) { 
    c = r;
  }
  else if (r * (r + 1) >= len){
    c = r + 1;
  }
  else {
    r = r + 1;
    c = r;
  }
  vvc grid;
  for (int i = 0; i < r; ++i) {
    vc row = vc(c, ' ');
    for (int j = 0; j < c; ++j) {
      if (j + i * c < len) {
        row[j] = s[j+i*c];
      }
    }
    grid.push_back(row);
  }
  string ans = "";
  for (int j = 0; j < c; ++j) {
    for (int i = 0; i < r; ++i) {
      char ch = grid[i][j];
      if (ch != ' ') {
        ans += ch;
      }
    }
    ans += ' ';
  }
  return ans;
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    string s;
    getline(cin, s);

    string result = encryption(s);

    fout << result << "\n";

    fout.close();

    return 0;
}
