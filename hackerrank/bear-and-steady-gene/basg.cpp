#include <string>
#include <iostream>
#include <fstream>
#include <unordered_map>

using namespace std;

bool isValid(
    unordered_map<char,int> map_to_deletes, 
    unordered_map<char,int> map_window) {
  string unique_genes = "ATCG";
  for (char& c: unique_genes) {
    if (map_window[c] < map_to_deletes[c]) {
      return false;
    }
  }
  return true;
}

int steadyGene(string gene) {
  unordered_map<char,int> map_counts;
  unordered_map<char,int> map_to_deletes;
  unordered_map<char,int> map_window;
  int t = gene.length() / 4;
  bool flag = true;
  for (char& c: gene) {
    map_counts[c]++;
  }
  for (auto const& c: map_counts) {
    map_to_deletes[c.first] = max(c.second - t, 0);
    flag = flag && (c.second == t);
  }
  if (flag) return 0;

  int l = 0;
  int r = 0;
  int min_val = 1000000000;
  while (r != gene.length()) {
    map_window[gene[r]]++;
    r++;
    while (isValid(map_to_deletes, map_window)) {
      min_val = min(min_val, r - l);
      cout << min_val << " " << l << " " << r << endl;
      map_window[gene[l]]--;
      l++;
    }
  }
  return min_val;
}

int main() {
  ifstream myfile;
  myfile.open("basg_c_1.in");
  int length;
  string gene;

  myfile >> length;
  myfile >> gene;

  int ans = steadyGene(gene);
  cout << ans << endl;
}

