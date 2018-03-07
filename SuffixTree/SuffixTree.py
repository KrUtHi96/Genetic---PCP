from SuffixTreeNode import SuffixTreeNode


class SuffixTree:
    def __init__(self, alphabet):
        self.root = None
        self.last_new_node = None

        # Active Point
        self.active_node = None
        self.active_edge = -1
        self.active_length = 0

        # Remaining suffix
        self.remainder = 0

        self.leaf_end = [-1]
        self.root_end = None
        self.split_end = None
        self.size = -1

        self.alphabet = alphabet

    def _get_new_node(self, start, end, string_number):
        node = SuffixTreeNode()

        for c in self.alphabet:
            node.children[c] = None

        node.suffix_link = self.root
        node.start = start
        node.end = end
        node.suffix_index = [-1, string_number]

        return node

    # Walk down procedure
    def walk_down(self, current_node):
        edge_length = current_node.edge_length()
        if (self.active_length >= edge_length):
            self.active_edge += edge_length
            self.active_length -= edge_length
            self.active_node = current_node
            return 1
        return 0

    # Extention procedure
    def extend_suffix_tree(self, position, text, string_number):
        self.leaf_end[0] = position
        self.remainder += 1
        self.last_new_node = None

        while self.remainder > 0:
            if self.active_length == 0:
                self.active_edge = position

            if self.active_node.children[text[self.active_edge]] == None:
                self.active_node.children[text[self.active_edge]] = self._get_new_node(position, self.leaf_end,
                                                                                       string_number)
                if self.last_new_node != None:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None

            else:
                next_node = self.active_node.children[text[self.active_edge]]
                if self.walk_down(next_node):
                    continue

                if text[next_node.start + self.active_length] == text[position]:
                    if self.last_new_node != None and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None

                    self.active_length += 1
                    break

                self.split_end = next_node.start + self.active_length - 1

                split = self._get_new_node(next_node.start, [self.split_end], string_number)
                self.active_node.children[text[self.active_edge]] = split

                split.children[text[position]] = self._get_new_node(position, self.leaf_end, string_number)
                next_node.start += self.active_length
                split.children[text[next_node.start]] = next_node

                if self.last_new_node != None:
                    self.last_new_node.suffix_link = split

                self.last_new_node = split

            self.remainder -= 1

            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = position - self.remainder + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link

    # Building suffix tree
    def build_suffix_tree(self, text, string_number):
        self.size = len(text)

        if self.root == None:
            self.root_end = [-1]
            self.root = self._get_new_node(-1, self.root_end, string_number)

        self.active_node = self.root
        for i in range(self.size):
            self.extend_suffix_tree(i, text, string_number)

        label_height = 0
        self.set_suffix_index_by_dfs(self.root, label_height, string_number)

    def build_generalized_suffix_tree(self, strings):
        self.strings = strings
        for i, text in enumerate(self.strings):
            self.build_suffix_tree(text, i)

    def set_suffix_index_by_dfs(self, n, label_height, string_number):
        if n == None:
            return

        if n.start != -1:
            pass
            # print(n.start, n.end[0])
            # print(self.strings[string_number][n.start:n.end[0] + 1], end="")

        leaf = 1
        for c in self.alphabet:
            if n.children[c] != None:
                child_node = n.children[c]
                if leaf == 1 and n.start != -1:
                    pass
                    # print(" [%d, %d]\n"%(n.suffix_index[0], n.suffix_index[1]))
                leaf = 0
                self.set_suffix_index_by_dfs(n.children[c], label_height + n.children[c].edge_length(), string_number)

        if leaf == 1:
            # Leaf node
            n.suffix_index = [self.size - label_height, string_number]
            # print(" [%d, %d]\n" % (n.suffix_index[0], n.suffix_index[1]))

    # Counting leaves
    def _traverse_to_leaf(self, node, occurences):
        if node == None:
            return 0

        if node.suffix_index[0] > -1:
            occurences.append(node.suffix_index[0])
            return 1

        count = 0
        for c in self.alphabet:
            if node.children[c] != None:
                count += self._traverse_to_leaf(node.children[c], occurences)

        return count

    # Counting all occurences
    def _find_all_positions(self, node, occurences):
        if node == None:
            return 0
        return self._traverse_to_leaf(node, occurences)

    # Traversing Edge according to pattern
    def _traverse_edge(self, pattern, index, start, end):
        for k in range(start, end + 1):
            if index == len(pattern):
                break

            if self.strings[0][k] != pattern[index]:
                return -1

            index += 1

        if index == len(pattern):
            return 1

        return 0

    # Traversing down the tree according to the pattern
    def _traverse_tree(self, node, pattern, index):
        if node == None:
            return -1, None

        result = -1
        occurences = []
        if node.start != -1:
            result = self._traverse_edge(pattern, index, node.start, node.end[0])
            if result == -1:
                # No match
                return -1, None
            if result == 1:
                # Found match
                if node.suffix_index[0] > -1:
                    occurences.append(node.suffix_index[0])
                else:
                    # Find others
                    self._find_all_positions(node, occurences)
                return 1, occurences

        # More characters to match
        index += node.edge_length()
        if node.children[pattern[index]] != None:
            return self._traverse_tree(node.children[pattern[index]], pattern, index)
        else:
            return -1, None

    # Pattern Matching - Buggy
    # Does not work for:
    # text = 'CAACTGGACCAACGCCCAAT'
    # pattern = 'CC'
    def find(self, pattern):
        ret_val, result = self._traverse_tree(self.root, pattern, 0)
        if ret_val != -1:
            return result
        return []


if __name__ == '__main__':
    alphabet = 'ACGT'
    t = SuffixTree(alphabet)

    '''
    text1 = 'AGCCTC$'
    text2 = 'CTCAGC#'
    t.build_generalized_suffix_tree([text1, text2])
    '''

    '''
    text = read_genome('../Dataset/phix.fa')
    t.build_generalized_suffix_tree([text])
    '''

    text = 'CAACTGGACCAACGCCCAAT'
    pattern = 'CC'
    t.build_generalized_suffix_tree([text])
    t.find(pattern)
