def sort_bucket(s, bucket, order):
    d = {}
    for i in bucket:
        key = s[i:i + order]

        if key not in d:
            d[key] = []

        d[key].append(i)

    result = []
    for k in sorted(d):
        v = d[k]
        if len(v) > 1:
            result += sort_bucket(s, v, order * 2)
        else:
            result.append(v[0])
    return result


def get_suffix_array(text):
    return sort_bucket(text, range(len(text)), 1)


def lcp_from_sa(text, suffix_array):
    n = len(suffix_array)

    lcp = [0] * n
    inv_suff = [0] * n

    for i in range(n):
        inv_suff[suffix_array[i]] = i

    k = 0
    for i in range(n):
        if inv_suff[i] == n - 1:
            k = 0
            continue

        j = suffix_array[inv_suff[i] + 1]
        while i + k < n and j + k < n and text[i + k] == text[j + k]:
            k += 1

        lcp[inv_suff[i]] = k

        if k > 0:
            k -= 1

    return lcp


def search(text, pattern, suffix_array, first_occurence=False, count=False, offset=0):
    left = 0
    right = len(suffix_array) - 1

    occurences = []

    m = len(pattern)

    while left <= right:
        middle = (left + right) // 2

        slice = text[suffix_array[middle]: suffix_array[middle] + m]
        # print(slice)

        if pattern == slice:
            occurences.append(offset + suffix_array[middle])
            cur = middle - 1
            while cur > -1 and text[suffix_array[cur]: suffix_array[cur] + m] == pattern:
                occurences.append(offset + suffix_array[cur])
                cur -= 1

            cur = middle + 1
            while cur < len(suffix_array) and text[suffix_array[cur]: suffix_array[cur] + m] == pattern:
                occurences.append(offset + suffix_array[cur])
                cur += 1

            if first_occurence:
                return min(occurences)

            if count:
                return len(occurences)

            return occurences
        elif pattern < slice:
            right = middle - 1
        else:
            left = middle + 1
    return []


if __name__ == '__main__':
    text = 'CAACTGGACCAACGCCCAAT'
    pattern = 'CC'
    suffix_array = get_suffix_array(text)
    print(search(text, pattern, suffix_array))
