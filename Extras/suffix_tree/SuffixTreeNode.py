class SuffixTreeNode:
    def __init__(self):
        self.children = {}
        self.suffix_link = None
        self.start = None
        self.end = None
        self.suffix_index = None

    def edge_length(self):
        return self.end[0] - self.start + 1


if __name__ == '__main__':
    pass
