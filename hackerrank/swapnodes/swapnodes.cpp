#include <iostream>
#include <queue>
#include <vector>
#include <fstream>

using namespace std;

typedef vector<vector<int>> vvi;
typedef vector<int> vi;

class Node {
  public:
    int value;
    Node* parent;
    Node* left;
    Node* right;
    Node() {
      value = 1;
      parent = NULL;
      left = NULL;
      right = NULL;
    }
    Node(int c_value, Node* c_parent) {
      value = c_value;
      parent = c_parent;
      left = NULL;
      right = NULL;
    }
    Node(int c_value, Node* c_parent, Node* c_left, Node* c_right) {
      value = c_value;
      parent = c_parent;
      left = c_left;
      right = c_right;
    }
};

class Tree {
  public:
    Node* root;
    Tree(vvi* p_indexes) {
      root = new Node();
      queue<Node*> my_queue;
      vvi indexes = *p_indexes;
      int l, r;
      my_queue.push(root);
      for (int i = 0; i < indexes.size(); ++i) {
        vi pair = indexes[i];
        l = pair[0];
        r = pair[1];
        Node* cur_node = my_queue.front();
        my_queue.pop();
        if (l != -1) {
          Node* new_node = new Node(l, cur_node);
          cur_node->left = new_node;
          my_queue.push(new_node);
        }
        if (r != -1) {
          Node* new_node = new Node(r, cur_node);
          cur_node->right = new_node;
          my_queue.push(new_node);
        }
      }
    }
    void PreOrder(Node* node) {
      if (node == NULL) {
        return;
      }
      PreOrder(node->left);
      PreOrder(node->right);
      cout << node->value << endl;
    }
    void InOrder(Node* node, vi* res) {
      if (node == NULL) {
        return;
      }
      InOrder(node->left, res);
      res->push_back(node->value);
      InOrder(node->right, res);
    }
};

void SwapTraverse(Node* node, int depth, int k) {
  ++depth;
  if (node->left == NULL && node->right == NULL) {
    return;
  }
  if (depth % k == 0) {
    Node* tmp = node->left;
    node->left = node->right;
    node->right = tmp;
  }
  if (node->left != NULL) {
    SwapTraverse(node->left, depth, k);
  }
  if (node->right != NULL) {
    SwapTraverse(node->right, depth, k);
  }
}

vvi swapNodes(vvi indexes, vi queries) {
  Tree* tree = new Tree(&indexes);
  cout << endl;
  vvi res;
  for (int i = 0; i < queries.size(); ++i) {
    SwapTraverse(tree->root, 0, queries[i]);
    vi row;
    tree->InOrder(tree->root, &row);
    res.push_back(row);
  }
  return res;
}

int main()
{
    ofstream fout(getenv("OUTPUT_PATH"));

    int n;
    cin >> n;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<vector<int>> indexes(n);
    for (int indexes_row_itr = 0; indexes_row_itr < n; indexes_row_itr++) {
        indexes[indexes_row_itr].resize(2);

        for (int indexes_column_itr = 0; indexes_column_itr < 2; indexes_column_itr++) {
            cin >> indexes[indexes_row_itr][indexes_column_itr];
        }

        cin.ignore(numeric_limits<streamsize>::max(), '\n');
    }

    int queries_count;
    cin >> queries_count;
    cin.ignore(numeric_limits<streamsize>::max(), '\n');

    vector<int> queries(queries_count);

    for (int queries_itr = 0; queries_itr < queries_count; queries_itr++) {
        int queries_item;
        cin >> queries_item;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');

        queries[queries_itr] = queries_item;
    }

    swapNodes(indexes, queries);
    vector<vector<int>> result = swapNodes(indexes, queries);

    for (int result_row_itr = 0; result_row_itr < result.size(); result_row_itr++) {
        for (int result_column_itr = 0; result_column_itr < result[result_row_itr].size(); result_column_itr++) {
            fout << result[result_row_itr][result_column_itr];

            if (result_column_itr != result[result_row_itr].size() - 1) {
                fout << " ";
            }
        }

        if (result_row_itr != result.size() - 1) {
            fout << "\n";
        }
    }

    fout << "\n";

    fout.close();

    return 0;
}
