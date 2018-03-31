import itertools

from DNAHelper import helper_functions


def pick_maximal_overlap(reads, k):
    reada, readb = None, None
    best_olen = 0

    for a, b in itertools.permutations(reads, 2):
        olen = helper_functions.overlap(a, b, min_len=k)
        # print(olen)
        if olen > best_olen:
            reada, readb = a, b
            best_olen = olen
    return reada, readb, best_olen


def greedy_scs(reads, k):
    read_a, read_b, olen = pick_maximal_overlap(reads, k)
    while olen > 0:
        reads.remove(read_a)
        reads.remove(read_b)
        reads.append(read_a + read_b[olen:])
        read_a, read_b, olen = pick_maximal_overlap(reads, k)

        print(len(reads))
    return ''.join(reads)


if __name__ == '__main__':
    reads, _ = helper_functions.read_fastq('Dataset/phix.fastq')
    print(reads)
    print(greedy_scs(reads, k=5))
