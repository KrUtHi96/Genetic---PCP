from DNAHelper.helper_functions import *
from SuffixTree import SuffixTree

alphabet = 'AGTCN'
text = read_genome('../Dataset/phix.fa')
reads, qualities = read_fastq('../Dataset/phix.fastq')

tree = SuffixTree(alphabet)
tree.build_generalized_suffix_tree([text])

count = 0
matches = []
for read in reads:
    read = read[:30]
    matches = tree.find(read)
    matches.extend(tree.find(reverse_complement(read)))
    if len(matches) > 0:
        count += 1
print(count, '/', len(reads), 'matched!')
