import get_titles
import time


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


def search(text, pattern, first_occurence=False, count=False, offset=0):
    start = time.time()
    suffix_array = get_suffix_array(text)
    end = time.time()
    print('Suffix array creation:', end - start)

    left = 0
    right = len(suffix_array) - 1

    occurences = []

    m = len(pattern)

    while left <= right:
        middle = (left + right) // 2;

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
    return -1


def search_in_range(text, pattern, in_range):
    start_string_len = len(in_range[0])
    end_string_len = len(in_range[1])

    start_index = search(text, in_range[0], first_occurence=True) + start_string_len
    end_index = search(text, in_range[1], first_occurence=True)

    return search(text[start_index: end_index], pattern, offset=start_index)


def get_maximal_palindrome(text):
    actual_len = len(text)

    new_text = text + '$' + text[::-1]
    # print(new_text)
    suffix_array = get_suffix_array(new_text)
    start = time.time()
    lcp = lcp_from_sa(new_text, suffix_array)
    end = time.time()

    print('LCP Array', end - start)
    longest_len = 0
    position = 0

    start = time.time()
    for i in range(1, len(lcp)):
        if (lcp[i] > longest_len):
            if (suffix_array[i] < actual_len and suffix_array[i + 1] > actual_len) or (
                            suffix_array[i + 1] < actual_len and suffix_array[i] > actual_len):
                longest_len = lcp[i]
                position = suffix_array[i]
    end = time.time()
    print('Maximal Palindrome', end - start)

    # print('Maximal palindrome is:', new_text[position : position + longest_len])
    # print('Length:', longest_len)
    # print('Position in', text, ':', len(new_text) - position - longest_len)

    return [new_text[position: position + longest_len], position]


def fill_indices(text, titles, search_algo):
    result = []
    prev_index = 0
    for title in titles:
        new_text = text[prev_index:]
        prev_index = search_algo(new_text, title, first_occurence=True, offset=prev_index)
        result.append((prev_index, title))
    return result


def Find_Maximal_Palindromes(text, PalindromeSize, in_range, algo):
    start_string_len = len(in_range[0])
    end_string_len = len(in_range[1])

    start_index = search(text, in_range[0], first_occurence=True) + start_string_len
    end_index = search(text, in_range[1], first_occurence=True)

    working_text = text[start_index: (end_index + len(in_range[1]))]
    titles = get_titles.get_titles(working_text)

    indexed_titles = fill_indices(working_text, titles, algo)

    result = []
    for i in range(len(indexed_titles) - 1):
        index1, title1 = indexed_titles[i]
        index2, title2 = indexed_titles[i + 1]
        result.append(
            (title1, get_palindromes(text[index1 + len(title1): index2], PalindromeSize, index1 + len(title1))))

    # Appending last title 'FOOTNOTES'
    last_title = indexed_titles[-1]
    index = last_title[0]
    result.append(
        (last_title[1], get_palindromes(text[index + len(last_title):], PalindromeSize, index + len(last_title))))

    for title, palindromes in result:
        if len(palindromes) != 0:
            print(title)
            for palindrome in palindromes:
                print('\t\t(Size:', len(palindrome), ') ', palindrome, ': ', palindromes[palindrome], sep='')
            print()


def get_palindromes(text, PalindromeSize, moving_index):
    maximal_palindromes = {}
    words = text.split()
    # print(words)
    for i in words:
        palindrome, position = get_maximal_palindrome(i)
        if len(palindrome) >= PalindromeSize:
            # print(max_pal_position[0])
            position += moving_index
            if palindrome not in maximal_palindromes:
                maximal_palindromes[palindrome] = []
            maximal_palindromes[palindrome].append(position)
        # print(i)
        moving_index += (len(i) + 1)
    return maximal_palindromes


if __name__ == '__main__':
    text = 'acaacaacawaca$'
    pattern = 'ac'
    # lcp = lcp_from_sa(text, suffix_array)
    found = search(text, pattern)

    print("Text:", text)
    print("Pattern:", pattern)
    # print("Suffix Array:", suffix_array)
    # print("LCP Array: ", lcp)
    print("Pattern occerences: ", found)
    print(search_in_range(text, 'aca', ('ac', 'w')))
    # get_maximal_palindrome(text, 3)
    print(get_maximal_palindrome("recognizing"))
    print(get_maximal_palindrome("indeed"))
    print(get_maximal_palindrome("ponno"))
