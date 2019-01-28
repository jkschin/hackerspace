#include <vector>
#include <iostream>
#include <algorithm>

using namespace std;

int main () {
  int num_cases;
  int i, j, n;
  long long c;
  cin >> num_cases;
  for (i = 0; i < num_cases; ++i) {
    cin >> n;
    vector <long long> arr1, arr2;
    for (j = 0; j < n; ++j) {
      cin >> c;
      arr1.push_back(c);
    }
    for (j = 0; j < n; ++j) {
      cin >> c;
      arr2.push_back(c);
    }
    sort(arr1.begin(), arr1.end());
    sort(arr2.begin(), arr2.end(), greater<long long>());
    long long ans = 0;
    for (j = 0; j < n; ++j) {
      ans += (arr1[j] * arr2[j]);
    }
    cout << "Case #" << (i + 1) << ": " << ans << endl;
  }
}
