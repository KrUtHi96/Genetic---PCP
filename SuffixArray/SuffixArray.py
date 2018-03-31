class SuffixArray:
    def __init__(self, text):
        self.text = text
        self.lcp = []
        self.suffix_array = []

        # Building suffix array and LCP array
        self._build_suffix_array()
        self._build_lcp_from_sa()

    def _sort_bucket(self, bucket, order):
        d = {}
        for i in bucket:
            key = self.text[i:i + order]

            if key not in d:
                d[key] = []

            d[key].append(i)

        result = []
        for k in sorted(d):
            v = d[k]
            if len(v) > 1:
                result += self._sort_bucket(v, order * 2)
            else:
                result.append(v[0])
        return result

    def _build_suffix_array(self):
        self.suffix_array = self._sort_bucket(range(len(self.text)), 1)

    def _build_lcp_from_sa(self):
        n = len(self.suffix_array)

        self.lcp = [0] * n
        inv_suff = [0] * n

        for i in range(n):
            inv_suff[self.suffix_array[i]] = i

        k = 0
        for i in range(n):
            if inv_suff[i] == n - 1:
                k = 0
                continue

            j = self.suffix_array[inv_suff[i] + 1]
            while i + k < n and j + k < n and self.text[i + k] == self.text[j + k]:
                k += 1

            self.lcp[inv_suff[i]] = k

            if k > 0:
                k -= 1

    def get_suffix_array(self):
        return self.suffix_array

    def get_lcp_array(self):
        return self.lcp

    def search(self, pattern, first_occurrence=False, count=False, offset=0):
        left = 0
        right = len(self.suffix_array) - 1

        occurrences = []

        m = len(pattern)

        while left <= right:
            middle = (left + right) // 2

            slice = self.text[self.suffix_array[middle]: self.suffix_array[middle] + m]
            # print(slice)

            if pattern == slice:
                occurrences.append(offset + self.suffix_array[middle])
                cur = middle - 1
                while cur > -1 and self.text[self.suffix_array[cur]: self.suffix_array[cur] + m] == pattern:
                    occurrences.append(offset + self.suffix_array[cur])
                    cur -= 1

                cur = middle + 1
                while cur < len(self.suffix_array) and self.text[
                                                       self.suffix_array[cur]: self.suffix_array[cur] + m] == pattern:
                    occurrences.append(offset + self.suffix_array[cur])
                    cur += 1

                if first_occurrence:
                    return min(occurrences)

                if count:
                    return len(occurrences)

                return occurrences
            elif pattern < slice:
                right = middle - 1
            else:
                left = middle + 1
        return []


if __name__ == '__main__':
    text = 'CAACTGGACCAACGCCCAAT'
    pattern = 'CC'
    suffix_array = SuffixArray(text)
    print(suffix_array.search(pattern))
