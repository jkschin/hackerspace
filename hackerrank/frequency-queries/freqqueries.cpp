#include <unordered_map>

using namespace std;

string ltrim(const string &);
string rtrim(const string &);
vector<string> split(const string &);

// Complete the freqQuery function below.
vector<int> freqQuery(vector<vector<int>> queries) {
  int query, val;
  unordered_map<int, int> freq;
  unordered_map<int, int> data;
  vector<int> ans;
  for (int i = 0; i < queries.size(); ++i) {
    query = queries[i][0];
    val = queries[i][1];
    if (query == 1) {
      if (data.find(val) != data.end()) {
        --freq[data[val]];
      }
      ++data[val];
      ++freq[data[val]];
    }
    else if (query == 2) {
      if (data.find(val) != data.end()) {
        --freq[data[val]];
        --data[val];
        ++freq[data[val]];
        if (data[val] == 0) {
          data.erase(val);
        }
      }
    }
    else if (query == 3) {
      if (freq[val] != 0) {
        ans.push_back(1);
      }
      else {
        ans.push_back(0);
      }
    }
  }
  return ans;
}
