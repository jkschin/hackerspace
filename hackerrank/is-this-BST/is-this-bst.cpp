/* Hidden stub code will pass a root argument to the function below. Complete the function to solve the challenge. Hint: you may want to write one or more helper functions.  

The Node struct is defined as follows:
	struct Node {
		int data;
		Node* left;
		Node* right;
*/

  bool Traverse(Node* node, int l, int u) {
    bool l_bool, r_bool;
    if (node->left == NULL && node->right == NULL) {
      return true;
    }
    if (node->data < 0 || node->data > 10000) {
      return false;
    }
    if (node->left != NULL) {
      if (node->left->data >= node->data || node->left->data <= l) {
        return false;
      }
      l_bool = Traverse(node->left, l, node->data);
    }
    if (node->right != NULL) {
      if (node->right->data <= node->data || node->right->data >= u) {
        return false;
      }
      r_bool = Traverse(node->right, node->data, u);
    }
    return l_bool && r_bool;
  }

  bool checkBST(Node* root) {
    return Traverse(root, 0, 10000);
  }
