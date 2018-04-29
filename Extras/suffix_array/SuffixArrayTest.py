from dna_utils.helper_functions import *
from Extras.suffix_array import SuffixArray

text = read_genome('../Dataset/phix.fa')
suffix_array = SuffixArray(text)

reads, qualities = read_fastq('../Dataset/phix.fastq')

count = 0
matches = []
for read in reads:
    read = read[:30]
    matches = suffix_array.search(read)
    matches.extend(suffix_array.search(reverse_complement(read)))
    if len(matches) > 0:
        count += 1
print(count, '/', len(reads), 'matched!')
