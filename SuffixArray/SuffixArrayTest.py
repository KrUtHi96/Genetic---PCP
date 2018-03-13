from SuffixArray import *
from DNAHelper.helper_functions import *

text = read_genome('../Dataset/phix.fa')
suffix_array = get_suffix_array(text)

reads, qualities = read_fastq('../Dataset/phix.fastq')

count = 0
matches = []
for read in reads:
    read = read[:30]
    matches = search(text, read, suffix_array)
    matches.extend(search(text, reverse_complement(read), suffix_array))
    if len(matches) > 0:
        count += 1
print(count, '/', len(reads), 'matched!')
