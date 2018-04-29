from __future__ import print_function
import sys

END_OF_STRING = sys.maxsize


class SuffixTreeNode:
    """
    Suffix tree node class. Also represents a tree edge that points to this node.
    """
    new_identifier = 0

    def __init__(self, start=0, end=END_OF_STRING, suffix_index=-1):
        self.identifier = SuffixTreeNode.new_identifier
        SuffixTreeNode.new_identifier += 1

        # suffix link is required by Ukkonen's algorithm
        self.suffix_link = None

        # child edges/nodes, each dict key represents the first letter of an edge
        self.edges = {}

        # stores reference to parent
        self.parent = None

        # bit vector shows to which strings this node belongs
        self.string_number = -1

        # edge info: start index and end index
        self.start = start
        self.end = end

        # Suffix index
        self.suffix_index = suffix_index

    def add_child(self, key, start, end, suffix_index):
        """
        :param key: a char that will be used during active edge searching
        :param start: node's edge start index
        :param end: node's edge end index
        :param suffix_index: suffix index of the string
        :return: created child node
        """

        child = SuffixTreeNode(start=start, end=end)
        child.parent = self
        child.suffix_index = suffix_index
        self.edges[key] = child
        return child

    def add_existing_node_as_child(self, key, node):
        """
        Add an existing node as a child
        Args:
            key: a char that will be used during active edge searching
            node: a node that will be added as a child
        """
        node.parent = self
        self.edges[key] = node

    def get_edge_length(self, current_index):
        """
        Get length of an edge that points to this node
        Args:
            current_index: index of current processing symbol (usefull for leaf nodes that have "infinity" end index)
        """
        return min(self.end, current_index + 1) - self.start

    def __str__(self):
        return 'id=' + str(self.identifier)


class SuffixTree:
    """
    Generalized suffix tree
    """

    def __init__(self):
        # the root node
        self.root = SuffixTreeNode(suffix_index=-1)

        # all strings are concatenated together. Tree's nodes stores only indices
        self.input_string = ''

        # number of strings stored by this tree
        self.strings_count = 0

        # list of tree leaves
        self.leaves = []

        # Terminal Symbol generator
        self.terminal_gen = self._terminal_symbols_generator()

    def append_string(self, input_string):
        """
        Add new string to the suffix tree
        """
        start_index = len(self.input_string)
        current_string_index = self.strings_count

        # each sting should have a unique ending
        input_string += next(self.terminal_gen)  # '$' + str(current_string_index)

        # gathering 'em all together
        self.input_string += input_string
        self.strings_count += 1

        # these 3 variables represents current "active point"
        active_node = self.root
        active_edge = 0
        active_length = 0

        # shows how many
        remainder = 0

        # new leaves appended to tree
        new_leaves = []

        # main circle
        for index in range(start_index, len(self.input_string)):
            previous_node = None
            remainder += 1
            while remainder > 0:
                if active_length == 0:
                    active_edge = index

                if self.input_string[active_edge] not in active_node.edges:
                    # no edge starting with current char, so creating a new leaf node
                    leaf_node = active_node.add_child(self.input_string[active_edge], index, END_OF_STRING, index)

                    # a leaf node will always be leaf node belonging to only one string
                    # (because each string has different termination)
                    leaf_node.string_number = current_string_index
                    new_leaves.append(leaf_node)

                    # doing suffix link magic
                    if previous_node is not None:
                        previous_node.suffix_link = active_node
                    previous_node = active_node
                else:
                    # ok, we've got an active edge
                    next_node = active_node.edges[self.input_string[active_edge]]

                    # walking down through edges (if active_length is bigger than edge length)
                    next_edge_length = next_node.get_edge_length(index)
                    if active_length >= next_node.get_edge_length(index):
                        active_edge += next_edge_length
                        active_length -= next_edge_length
                        active_node = next_node
                        continue

                    # current edge already contains the suffix we need to insert.
                    # Increase the active_length and go forward
                    if self.input_string[next_node.start + active_length] == self.input_string[index]:
                        active_length += 1
                        if previous_node is not None:
                            previous_node.suffix_link = active_node
                        previous_node = active_node
                        break

                    # splitting edge
                    split_node = active_node.add_child(
                        self.input_string[active_edge],
                        next_node.start,
                        next_node.start + active_length,
                        index
                    )
                    next_node.start += active_length
                    split_node.add_existing_node_as_child(self.input_string[next_node.start], next_node)
                    leaf_node = split_node.add_child(self.input_string[index], index, END_OF_STRING, index)
                    leaf_node.string_number = current_string_index
                    new_leaves.append(leaf_node)

                    # suffix link magic again
                    if previous_node is not None:
                        previous_node.suffix_link = split_node
                    previous_node = split_node

                remainder -= 1

                # follow suffix link (if exists) or go to root
                if active_node == self.root and active_length > 0:
                    active_length -= 1
                    active_edge = index - remainder + 1
                else:
                    active_node = active_node.suffix_link if active_node.suffix_link is not None else self.root

        # update leaves ends from "infinity" to actual string end
        for leaf in new_leaves:
            leaf.end = len(self.input_string)
        self.leaves.extend(new_leaves)

    # Try : 1
    def _dfs_helper(self, node, string_depth, string_len):
        if string_depth == string_len:
            print('Node ID: {0}\nString Number: {1:b}\nSuffix Number: {2}'.format(node, int(str(node.bit_vector), 1),
                                                                                  node.suffix_index))  # , node.start, node.end, string_depth)

        for key in node.edges:
            # if not node.edges[key]._visited: # Not required as a tree cannot have 2 PARENTS having the same CHILD XD
            self._dfs_helper(node.edges[key], string_depth + node.edges[key].get_edge_length(END_OF_STRING), string_len)

    def dfs(self, string_len):
        self._dfs_helper(self.root, 0, string_len)

    # Try : 2
    def _get_leaves(self, node, strings):
        for key in node.edges:
            curr_node = node.edges[key]
            if curr_node.edges:
                self._get_leaves(curr_node, strings)
            else:
                strings.append(curr_node.string_number)

    def overlap(self, current_string_num, string, min_overlap=0, verbose=False):
        index = 0
        current_node = self.root
        max_overlaps = [0] * self.strings_count
        while index < len(string):
            if verbose:
                print(index)
                print(current_node)

            next_node = current_node.edges[string[index]]
            index += next_node.get_edge_length(END_OF_STRING)
            current_node = next_node

            # Finding Leaf nodes
            strings = []
            for key in current_node.edges:
                if key not in ['A', 'G', 'T', 'C']:
                    strings.append(current_node.edges[key].string_number)

            for str_num in strings:
                if str_num != current_string_num and index >= min_overlap and index > max_overlaps[str_num]:
                    max_overlaps[str_num] = index
        '''
            if '$' in current_node.edges:
                node = current_node.edges['$']

                # Ending at more than 1 string
                if node.edges:
                    for key in node.edges:
                        leaf_node = node.edges[key]

                        # Update Max Overlap for nodes
                        string_num = leaf_node.string_number
                        if string_num != current_string_num and index > max_overlaps[string_num]:
                            max_overlaps[string_num] = index

                            if verbose:
                                print('\n***************LEAF IN PATH***************')
                                print('Node ID: {}\nString Number: {}\nSuffix Number: {}\nOverlap: {}'.format(
                                            leaf_node,
                                            string_num, 
                                            leaf_node.suffix_index,
                                            max_overlaps[string_num]
                                        )
                                    )
                                print('******************************************\n')
                # Ending at 1 string
                else:
                    if verbose:
                        print(node)
                        print(node.string_number)

                    # Update Max Overlap for nodes
                    string_num = node.string_number
                    if index > max_overlaps[string_num]:
                        max_overlaps[string_num] = index

                        if verbose:
                            print('\n***************LEAF IN PATH***************')
                            print('Node ID: {}\nString Number: {}\nSuffix Number: {}\nOverlap: {}'.format(
                                        node,
                                        string_num, 
                                        node.suffix_index,
                                        max_overlaps[string_num]
                                    )
                                )
                            print('******************************************\n')

        index -= 1 # Go back to remove $
        for key in current_node.edges:
            leaf_node = current_node.edges[key]

            # Update Max Overlap for nodes
            string_num = leaf_node.string_number
            if string_num != current_string_num and index > max_overlaps[string_num]:
                max_overlaps[string_num] = index

                if verbose:
                    print('\n***************LEAF IN PATH***************')
                    print('Node ID: {}\nString Number: {}\nSuffix Number: {}\nOverlap: {}'.format(
                                leaf_node,
                                string_num, 
                                leaf_node.suffix_index,
                                max_overlaps[string_num]
                            )
                        )
                    print('******************************************\n')
        '''
        return max_overlaps

    def _terminal_symbols_generator(self):
        """Generator of unique terminal symbols used for building the Generalized Suffix Tree.
        Unicode Private Use Area U+E000..U+F8FF is used to ensure that terminal symbols
        are not part of the input string.
        """
        UPPAs = list(
            list(range(0xE000, 0xF8FF + 1)) + list(range(0xF0000, 0xFFFFD + 1)) + list(range(0x100000, 0x10FFFD + 1)))
        for i in UPPAs:
            yield (chr(i))
        raise ValueError("Too many input strings.")

    def to_graphviz(self, node=None, output=''):
        """
        Show the tree as graphviz string. For debugging purposes only
        """
        if node is None:
            node = self.root
            output = 'digraph G {edge [arrowsize=0.4,fontsize=10];'

        output += \
            str(node.identifier) + '[label="' + \
            str(node.identifier) + '\\n' + '{}'.format(node.string_number) + '"'
        # if node.bit_vector == 2 ** self.strings_count - 1:
        #    output += ',style="filled",fillcolor="red"'
        output += '];'
        if node.suffix_link is not None:
            output += str(node.identifier) + '->' + str(node.suffix_link.identifier) + '[style="dashed"];'

        for child in node.edges.values():
            label = self.input_string[child.start:child.end]
            output += str(node.identifier) + '->' + str(child.identifier) + '[label="' + label + '"];'
            output = self.to_graphviz(child, output)

        if node == self.root:
            output += '}'

        return output

    def __str__(self):
        return self.to_graphviz()
