import numpy as np


class OverlapScorePigeonhole:

    def __init__(self, reads, overlap_minimum=12, max_error=3):

        self.overlap_minimum = overlap_minimum
        self.max_error = max_error

        self.n_pieces = max_error + 1
        self.piece_size = self.overlap_minimum // self.n_pieces

        self.reads = reads
        self.n_reads = len(reads)

        self.read_len = len(reads[0])

    def divide(self, text):
        pieces = [text[i: i + self.piece_size] for i in range(0, self.overlap_minimum, self.piece_size)]

        return pieces

    def build_index(self):

        index = [None] * self.n_pieces
        read_n = 1

        for read in self.reads:
            for i in range(self.n_pieces):

                start = i * self.piece_size

                piece = read[start:start + self.piece_size]

                if index[i] == None:
                    index[i] = {}
                if piece not in index[i]:
                    index[i][piece] = []

                index[i][piece].append(read_n)
            read_n += 1
        return index

    def get_suffixes(self, read):

        N = self.read_len
        suffixes = [read[i:] for i in range(N - self.overlap_minimum + 1)]

        return suffixes

    def overlap_scores(self):

        matrix = np.zeros(shape=[self.n_reads, self.n_reads])

        index = self.build_index()

        for read_index in range(self.n_reads):

            for S in self.get_suffixes(self.reads[read_index]):

                pieces = self.divide(S[:self.overlap_minimum])

                for i in range(self.n_pieces):

                    if pieces[i] in index[i]:

                        Li = index[i][pieces[i]]

                        for read_no in Li:

                            temp, end = 0, (i * self.piece_size)
                            s1, s2 = S[:end], self.reads[read_no - 1][:end]

                            for char_index in range(end):
                                if (s1[char_index] != s2[char_index]):
                                    temp += 1

                            if temp < self.max_error:

                                temp1, reached_end, start = 0, True, i * self.piece_size + self.piece_size
                                s1, s2 = S[start:], self.reads[read_no - 1][start:]

                                for char_index in range(len(s1)):
                                    if temp1 == self.max_error:
                                        reached_end = False
                                        break
                                    if s1[char_index] != s2[char_index]:
                                        temp1 += 1

                                if (reached_end) and (temp1 < self.max_error):
                                    if read_index + 1 != read_no:
                                        score = len(S)
                                        matrix[read_index, read_no - 1] = score - temp
                                        # print(read_index + 1," -> ", read_no, "Score :", score, "Error : ", temp)

                        break
        return matrix


if __name__ == '__main__':
    reads = [
        'AACCTTTCACGGTCACCCGCGG',
        'TTTCACGGTCACCCAGTCAACC',
        'GGTTAAACCCGGTAACCGTCAT',
        'AACCTTGTGCTCCCAACGTAAA',
        'GGTTCCAAACACTTGGTCAATC',
        'TTGGAACCTTTCACGGTCACCC'
    ]

    for read in reads:
        print(read)

    osp = OverlapScorePigeonhole(reads)

    matrix = osp.overlap_scores()

    print("\n", matrix)
