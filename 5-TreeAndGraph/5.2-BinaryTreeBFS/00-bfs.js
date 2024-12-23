// JS doesn't support a built-in efficient queue
//
// => Use 2 arrays:
// - a primary array (queue) for nodes of the current level
// - a secondary array (nextQueue) for nodes of the next level
// -> reassign nextQueue to queue after processing the current level
//    (avoid shifting elements when dequeue)

class TreeNode {
  constructor(val, left = null, right = null) {
    this.val = val;
    this.left = left;
    this.right = right;
  }
}

function bfs(root) {
  // Handle empty tree
  if (!root) {
    return;
  }

  // Add the root node to the primary queue
  let queue = [root];

  while (queue.length > 0) {
    // Use nextQueue to collect nodes of the next level
    const nextQueue = [];

    for (const node of queue) {
      // Process current node
      console.log(node.val);

      // Enqueue the children if they exist
      if (node.left) {
        nextQueue.push(node.left);
      }
      if (node.right) {
        nextQueue.push(node.right);
      }
    }

    // Move to the next level
    queue = nextQueue;
  }
}
